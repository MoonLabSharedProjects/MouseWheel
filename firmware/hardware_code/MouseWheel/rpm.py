import RPi.GPIO as GPIO
import csv
import time
import sys
from time import sleep
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

with open('wheeldata.csv','w') as newFile:
    newFileWriter = csv.writer(newFile)
    newFileWriter.writerow(['Time', 'Interval', 'Distance', 'Weight', 'RFID', 'Top Speed'])

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

def my_callback(channel):
     print "cool"

GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback)

while True:
    try:
        pass
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()