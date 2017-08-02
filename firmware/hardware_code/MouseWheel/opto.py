import RPi.GPIO as GPIO
from time import sleep
import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.IN)

counter = 0

def my_callback(channel):
     global counter
     counter += 1
     print counter

GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback)

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
