import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

class Rotate:
    def __init__(self):
        self.RotEnable = 35
        self.RotClkPin = 40
        self.RotDirPin = 38
        self.Rot_PULSE_TIME = 0.001
        gpio.setup(self.RotEnable, gpio.OUT)
        gpio.setup(self.RotClkPin, gpio.OUT)
        gpio.setup(self.RotDirPin, gpio.OUT)
        gpio.output(self.RotEnable, True)

    def pulseRot(self, x, y):
        gpio.output(self.RotDirPin, x)
        for i in range (y):
            for i in range(500):
                gpio.output(self.RotClkPin, True)
                time.sleep(self.Rot_PULSE_TIME)
                gpio.output(self.RotClkPin, False)

class Auger:
    def __init__(self):
        self.AugEnable = 7
        self.AugClkPin = 29
        self.AugDirPin = 31
        self.Aug_PULSE_TIME = 0.001
        gpio.setup(self.AugEnable, gpio.OUT)
        gpio.setup(self.AugClkPin, gpio.OUT)
        gpio.setup(self.AugDirPin, gpio.OUT)
        gpio.output(self.AugEnable, True)

    def pulseAug(self, x, y):
        gpio.output(self.AugDirPin, x)
        for i in range (y):
            for i in range(500):
                gpio.output(self.AugClkPin, True)
                time.sleep(self.Aug_PULSE_TIME)
                gpio.output(self.AugClkPin, False)

class Spoon:

    def __init__(self):
        self.SpEnable = 32
        self.SpClkPin = 46
        self.SpDirPin = 33
        self.Sp_PULSE_TIME = 0.001
        gpio.setup(self.SpEnable, gpio.OUT)
        gpio.setup(self.SpClkPin, gpio.OUT)
        gpio.setup(self.SpDirPin, gpio.OUT)
        gpio.output(self.SpEnable, True)

    def pulseSp(self, x, y):
        gpio.output(self.SpDirPin, x)
        for i in range (y):
            for i in range(500):
                gpio.output(self.SpClkPin, True)
                time.sleep(self.Sp_PULSE_TIME)
                gpio.output(self.SpClkPin, False)

