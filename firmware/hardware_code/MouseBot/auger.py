import RPi.GPIO as gpio
import time

AugEnable = 7
AugClkPin = 29
AugDirPin = 31
AUG_PULSE_TIME = 0.001

def initialiseAug():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(AugEnable, gpio.OUT)
    gpio.setup(AugClkPin, gpio.OUT)
    gpio.setup(AugDirPin, gpio.OUT)
    gpio.setup(16, gpio.IN)
    gpio.output(AugEnable, True)

def pulseAug(x, y):
    gpio.output(AugDirPin, x)
    for i in range (y):
        for i in range(500):
            gpio.output(AugClkPin, True)
            time.sleep(AUG_PULSE_TIME)
            gpio.output(AugClkPin, False)

def dispenseOne():
    while gpio.input(16) == 0:
        pulseAug(False, 5)
        pulseAug(True, 1)
    print "one sugar pellet dispensed"
    gpio.cleanup()

initialiseAug()
dispenseOne()
