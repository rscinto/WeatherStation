# Needed modules will be imported and configured 
from datetime import date
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)
  
# The input pin which is connected with the sensor
GPIO_PIN = 16
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
readings = 0
maxReadings = 25
timeOne = 0.0 
timeTwo = 0.0 
timeDifference = 0.0 
phase = 1




#prompt user to start
print("Speed Test")
#maxReadings = input("Number of Readings: ")
print("Test Ready...")

#test
#print("MAX READINGS: ", str(maxReadings))






#tire circumference in milli meters
tireCircumference = 125.6637061
anemometerCircumference = 169.6460033

def outputFunction(null):
    global readings
    global timeOne
    global timeTwo
    global timeDifference
    global phase
    global tireCircumference
    global anemometerCircumference
    global maxReadings

    print("Reading: ", str(readings))
    
    if readings == 0:
        #Start the clock after first reading
        timeOne = time.perf_counter_ns()
        print("Test Started")
        print("     Sample 1: ", str(timeOne))
    
    if readings == maxReadings:
        #Max readings has been achieved and the time data is processed. 
        timeTwo = time.perf_counter_ns()
        timeDifference = timeTwo - timeOne
        print("     Sample 2: ", str(timeTwo))
        print("Test Complete")
        print("Time for readings (Nano Seconds): ", str(timeDifference))
        print("Time for readings  (Seconds): ", str(timeDifference / 1000000000))
        print("DC motor Speed (mm/s): ", str((tireCircumference*readings)/(timeDifference / 1000000000)))
        print("Anemometer Speed (mm/s): ", str((anemometerCircumference*readings)/(timeDifference / 1000000000)))
        quit()

    readings = readings + 1

  
# signal detection (raising edge).
GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=outputFunction, bouncetime=100) 






# Main program loop
try:
        while True:
                time.sleep(1)
  
# Scavenging work after the end of the program
except KeyboardInterrupt:
        GPIO.cleanup()