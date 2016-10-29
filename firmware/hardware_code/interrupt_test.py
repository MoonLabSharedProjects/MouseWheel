import RPi.GPIO as GPIO
import datetime
class Interrupt:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.event_callback, bouncetime=200)
    def event_callback(self, channel):
        print datetime.datetime.now()


Interrupt()

try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()