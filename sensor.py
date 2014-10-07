#!/usr/bin/python

import spidev
import RPi.GPIO as GPIO
import datetime
import time
import os
import sensor_logins as Logins
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCDPlate()

import plotly.plotly as plot
from plotly.graph_objs import *

sensors = 6
reading_delay = 3
plot_delay = 600
min_moisture = 966 #~3.11V instead of 1023@3.3V
max_moisture = 0
diff_moisture = min_moisture - max_moisture
readings = [0] * sensors
plot_data = [''] * sensors
script_running = False

plotly_username = Logins.GetPlotlyUsername()
plotly_api_key = Logins.GetPlotlyApiKey()
plot.sign_in(plotly_username, plotly_api_key)
plot_layout = Layout(
    title='Indoor Garden Water Sensor Data'
)

spi = spidev.SpiDev()
spi.open(0, 0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, False)

def ReadChannel(channel):
	adc = spi.xfer2([1, (8 + channel) << 4, 0])
	data = ((adc[1] & 3) << 8) + adc[2]
	return data

def GetPercent(moisture_level):
	percent = (min_moisture - moisture_level) * 100 / diff_moisture
	if percent > 100:
		percent = 100
	if percent < 0:
		percent = 0
	return percent

def RotateReadings():
	#lcd.display()
	for i in range(sensors):
		moisture_level = readings[i]
		moisture_percent = GetPercent(moisture_level)
		reading = 'Pot: {} ({})\nMoisture {}%'.format(i +1, moisture_level, moisture_percent)
		print(reading)
		lcd.clear()
		lcd.message(reading)
		time.sleep(reading_delay)
	lcd.clear()
	#lcd.noDisplay()

while True:
	GPIO.output(7, True)
	time.sleep(0.1)

	curr_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	for i in range(sensors):
		readings[i] = ReadChannel(i)
		
		plot_data[i] = Scatter(
			x = [curr_date_time],
			y = [GetPercent(readings[i])],
			name = 'Pot ' + str(i + 1)
		)

		time.sleep(0.1)
	
	GPIO.output(7, False)

	script_running = True

	try:
		plot_url = plot.plot(Data(plot_data), filename='water-sensors', fileopt='extend', layout=plot_layout, auto_open=False)
	except:
		pass

	RotateReadings()

	time.sleep(plot_delay)