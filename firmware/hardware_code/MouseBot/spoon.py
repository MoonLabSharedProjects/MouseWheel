import RPi.GPIO as gpio
import time

SpEnable = 32
SpClkPin = 36
SpDirPin = 33

Sp_PULSE_TIME = 0.001

def initialiseSpoon():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(SpEnable, gpio.OUT)
    gpio.setup(SpClkPin, gpio.OUT)
    gpio.setup(SpDirPin, gpio.OUT)
    gpio.setup(12, gpio.IN)
    gpio.output(SpEnable, True)

def pulseSpoon(x, y):
    gpio.output(SpDirPin, x)
    for i in range (y):
        for i in range(500):
            gpio.output(SpClkPin, True)
            time.sleep(Sp_PULSE_TIME)
            gpio.output(SpClkPin, False)

initialiseSpoon()

while gpio.input(12) == 0:
    pulseSpoon(False, 1)
pulseSpoon(True, 1)