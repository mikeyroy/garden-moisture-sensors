#!/usr/bin/python

import time
import config

import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCDPlate()

buttons = ((LCD.SELECT, 'Select', (1,0,0)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (1,0,0)),
            (LCD.DOWN,   'Down'  , (1,0,0)),
            (LCD.RIGHT,  'Right' , (1,0,0)))

def GetPercent(moisture_level):
	percent = (config.min_moisture - moisture_level) * 100 / config.diff_moisture
	if percent > 100:
		percent = 100
	if percent < 0:
		percent = 0
	return percent

def RotateReadings():
	for i in range(config.sensors):
		moisture_level = config.readings[i]
		moisture_percent = GetPercent(moisture_level)
		reading = 'Pot: {} ({})\nMoisture {}%'.format(i +1, moisture_level, moisture_percent)
		print(reading)
		lcd.clear()
		lcd.message(reading)
		time.sleep(config.reading_delay)
	lcd.clear()
