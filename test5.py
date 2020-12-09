#!/usr/bin/env python3

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

#
import RPi.GPIO as GPIO
from signal import pause
#import dht11
import math
#

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

#
import sys
#import adafruit_dht
import board
import pigpio
#dhtDevice = adafruit_dht.DHT11(board.D4)
#dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
#
import DHT
import time
import datetime

sensor = DHT.DHT11
pin = 4     # Data - Pin 7 (BCM 4)





# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)


ObstaclePin     = 21 
LED_red         = 20 
num_readings    = 0
time_even       = 0.0
time_odd        = 0.0
time_difference = 0.0
temperature 	= 0.0
humidity 		= 0.0


pi = pigpio.pi()

s = DHT.sensor(pi, pin, model = sensor)

def setup():
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
	GPIO.setwarnings(False)
	GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(LED_red,GPIO.OUT)




def loop():
	while True:
		global temperature
		global humidity

		timestamp, gpio, status, temperature, humidity = s.read()   #read DHT device

		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		# Write two lines of text.
		draw.text((x, top),       "Weather Station ",  font=font, fill=255)
		draw.text((x, top+8),     "Temperature:   C " + str(temperature),  font=font, fill=255)
		draw.text((x, top+16),    "Wind Speed: kts ",  font=font, fill=255)
		draw.text((x, top+25),    "Humidity:      % " + str(humidity),  font=font, fill=255)

		# Display image.
		disp.image(image)
		disp.display()
		time.sleep(.1)

		if (0 == GPIO.input(ObstaclePin)):
			global num_readings
			global time_even
			global time_odd
			global time_difference
			
			print("Sensor detected")
			GPIO.output(LED_red,GPIO.HIGH)
			GPIO.output(LED_red,GPIO.LOW)
			num_readings += 1
			print("Number of Readings ", num_readings)
			if ((num_readings % 2) == 0):
				time_even = time.time()
				print("Even Time: ", time_even)
			else:
				time_odd = time.time()
				print("Odd Time: ", time_odd)
			time_difference = abs(time_even - time_odd)
			print("Time Difference: ", time_difference)


def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()