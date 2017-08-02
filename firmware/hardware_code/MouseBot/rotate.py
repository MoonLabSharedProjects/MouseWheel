import RPi.GPIO as gpio
import time

RotEnable = 35
RotClkPin = 40
RotDirPin = 38

Rot_PULSE_TIME = 0.001

def initialiseRot():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(RotEnable, gpio.OUT)
    gpio.setup(RotClkPin, gpio.OUT)
    gpio.setup(RotDirPin, gpio.OUT)
    gpio.setup(11, gpio.IN)
    gpio.output(RotEnable, True)

def pulseRot(x, y):
    gpio.output(RotDirPin, x)
    for i in range (y):
        for i in range(500):
            gpio.output(RotClkPin, True)
            time.sleep(Rot_PULSE_TIME)
            gpio.output(RotClkPin, False)

initialiseRot()

while gpio.input(11) == 0:
    pulseRot(False, 1)
pulseRot(True, 1)