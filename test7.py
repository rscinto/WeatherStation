#!/usr/bin/env python3

#OLED Display
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import board
#END OLED Display



#DHT11 
import RPi.GPIO as GPIO
import pigpio #DHT11 Daemon
import DHT

sensor = DHT.DHT11
pi = pigpio.pi()
pin = 23     # Data for Temperature and Humidity
s = DHT.sensor(pi, pin, model = sensor)
temperature 	= 0.0
humidity 		= 0.0
#END DHT11 

#Magnet sensor
GPIO_PIN = 24
readings = 0
maxReadings = 25
timeOne = 0.0 
timeTwo = 0.0 
timeDifference = 0.0

#Signal Light
LED_red         = 20 

#meters per second
windSpeed = 0.0 

#millimeters
anemometerCircumference = 169.6460033 

def outputFunction(null):

    global readings
    global timeOne
    global timeTwo
    global timeDifference
    global anemometerCircumference
    global maxReadings
    global windSpeed
    global temperature
    global humidity

    print("Wind Sensor Tripped")
    GPIO.output(LED_red,GPIO.HIGH)

    if readings == maxReadings:
        timeTwo = time.perf_counter_ns()
        timeDifference = timeTwo - timeOne                     
        print("Batch Complete")
        print("Time for readings (Nano Seconds): ", str(timeDifference))
        print("Time for readings  (Seconds): ", str(timeDifference / 1000000000))
        print("Anemometer Speed (mm/s): ", str((anemometerCircumference*readings)/(timeDifference / 1000000000)))
        print("Temperature: C", str(temperature))
        print("Humidity: %", str(humidity))
        
        windSpeed = (anemometerCircumference*readings)/(timeDifference / 1000000000) / 1000
        readings = 0
    elif readings == 0:
        timeOne = time.perf_counter_ns()
        readings += 1
        print("Reading: ", str(readings))
    else:
        readings += 1
        print("Reading: ", str(readings))


#OLED Display
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
#END OLED Display





#Functions
def setup():
    # Numbers GPIOs by physical location
    GPIO.setmode(GPIO.BCM)       
    GPIO.setwarnings(False)

    #Wind Signal Detected LED
    GPIO.setup(LED_red,GPIO.OUT)

    # signal detection (raising edge).
    #Magnet sensor
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=outputFunction, bouncetime=100) 
        

def loop():
    while True:
        global temperature
        global humidity  
        global GPIO_PIN
        GPIO.output(LED_red,GPIO.LOW)

        #this sleep is interupted after every signal transmission from the magenet sensor
        time.sleep(1)

        timestamp, gpio, status, temperature, humidity = s.read()   #read DHT device

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        #convert to knots
        # wind speed at m/s at this point 
        knots = round(windSpeed * 1.944, 2)
        

        # Write 4 lines of text.
        draw.text((x, top),       "Weather Station ",  font=font, fill=255)
        draw.text((x, top+8),     "Temperature:   C " + str(temperature),  font=font, fill=255)
        draw.text((x, top+16),    "Wind: kts " + str(knots), font=font, fill=255)
        draw.text((x, top+25),    "Humidity:      % " + str(humidity),  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()

def destroy():
	GPIO.cleanup()                     # Release resource
#ENDFunctions


#Main   

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
#END Main