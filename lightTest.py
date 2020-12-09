import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module

redLED = 20

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(redLED, GPIO.OUT) # Set pin 8 to be an output pin and set initial value to low (off)

while True: # Run forever
 GPIO.output(redLED, GPIO.HIGH) # Turn on
 sleep(1) # Sleep for 1 second
 GPIO.output(redLED, GPIO.LOW) # Turn off
 sleep(1) # Sleep for 1 second