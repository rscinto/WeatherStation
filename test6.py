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

#import subprocess

#
#import sys
import board
import pigpio
import DHT
import time
import datetime

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
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



LED_red         = 20 
num_readings    = 0
time_even       = 0.0
time_odd        = 0.0
time_difference = 0.0
temperature 	= 0.0
humidity 		= 0.0

sensor = DHT.DHT11
pi = pigpio.pi()
pin = 4     # Data - Pin 7 (BCM 4)
s = DHT.sensor(pi, pin, model = sensor)

#Magnet sensor
GPIO_PIN = 16


def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setwarnings(False)
    GPIO.setup(LED_red,GPIO.OUT)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=outputFunction, bouncetime=100) 

# function called when sensor is tripped
def outputFunction(null):
        global num_readings
        print("Sensor is blocked")
        GPIO.output(LED_red,GPIO.HIGH)
        num_readings += num_readings



def loop():
    while True:
        global temperature
        global humidity  
        global GPIO_PIN
        GPIO.output(LED_red,GPIO.LOW)

        time.sleep(2)


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





def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()