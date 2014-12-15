garden-moisture-sensors
=======================

Monitors soil moisture levels using a Raspberry Pi, MCP3008, individual moisture sensors, and charts it to Plot.ly

Requires another file named `sensor_logins.py` and a plot.ly account
```
#!/usr/bin/python

def GetPlotlyUsername()
	return 'yourplotlyusername'
	
def GetPlotlyApiKey()
	return 'yourapikey'
```

#Enable SPI on your Raspberry Pi
`sudo nano /etc/modprobe.d/raspi-blacklist.conf`

Make sure there is a # before blacklist spi-bcm2708

`#blacklist spi-bcm2708`

#Install prerequisites
```
sudo apt-get update
sudo apt-get install python-dev
sudo apt-get install python-rpi.gpio

git clone git://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install

pip install plotly
```

#Run project
`sudo python sensor.py`
