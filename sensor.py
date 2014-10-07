#!/usr/bin/python

import spidev
import RPi.GPIO as GPIO
import datetime
import time
import os
from threading import Thread
import sensor_logins as Logins
import lcd_readout as Readout
import config

import plotly.plotly as plot
from plotly.graph_objs import *

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

def RunSensors():
	while True:
		GPIO.output(7, True)
		time.sleep(0.1)
	
		curr_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
		for i in range(config.sensors):
			config.readings[i] = ReadChannel(i)
			
			config.plot_data[i] = Scatter(
				x = [curr_date_time],
				y = [Readout.GetPercent(config.readings[i])],
				name = 'Pot ' + str(i + 1)
			)
	
			time.sleep(0.1)
		
		GPIO.output(7, False)
	
		try:
			plot_url = plot.plot(Data(config.plot_data), filename='water-sensors', fileopt='extend', layout=plot_layout, auto_open=False)
		except:
			pass
		
		Readout.RotateReadings()
	
		time.sleep(config.plot_delay)

runSensorsThread = Thread(target = RunSensors)
runSensorsThread.start()

while True: #keep the script alive so it can cancel the threads with Ctrl+c
	time.sleep(1)