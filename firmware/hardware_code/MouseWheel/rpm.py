import RPi.GPIO as GPIO
import time
import sys
from time import sleep
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

times = []
rpm1 = []
blixed = [1, 2, 3]

def cleanAndExit():

    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

def my_callback(channel):
     global times
     global rpm1
     a = time.time()
     times.append(a)
     if len(times) > 2:
         b = times[1] - times[0]
         c = b * 36
         rpm = 60/c
         del times[0]
         rpm1.append(round(rpm,1))

GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback)

while True:
    try:
        if len(rpm1) > 2:
            x = blixed[len(blixed)-1]
            y = blixed[len(blixed)-2]
            if x == y:
                print "0 RPM"
            else:
                print str(rpm1[len(rpm1)-1]) + " RPM"
            blixed.append(rpm1[len(rpm1)-2])
            del blixed[0]
        else:
            print "0 RPM"
        sleep(0.3)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()