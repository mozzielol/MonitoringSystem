import pyupm_grove
import pyupm_th02 as upmTh02

import mraa
import time
import sys

LIGHT_SENSOR_PIN= 2
light = pyupm_grove.GroveLight(LIGHT_SENSOR_PIN)


def light_sensor():
    return light.value()

class TemperatureAndHumiditySensor:
	def __init__(self,bus):
		self.th02_sensor = upmTh02.TH02(bus)
		self.temperature_celsius = 0.0
		self.temperature_fahrenheit = 0.0
		self.humidity = 0.0

	def measure_temperature_and_humidity(self):
		temperature_celsius = self.th02_sensor.getTemperature()
		self.temperature_celsius = temperature_celsius
		self.temperature_fahrenheit = \
		(temperature_celsius*9.0/5.0)+32
		self.humidity = self.th02_sensor.getHumidity()