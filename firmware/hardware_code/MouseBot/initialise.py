from stepper import Rotate, Auger, Spoon
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

chute_pin = 16
spoon_home_pin = 12
rotate_home_pin = 11

def SensorInit():
    gpio.setup(chute_pin, gpio.IN)
    gpio.setup(spoon_home_pin, gpio.IN)
    gpio.setup(rotate_home_pin, gpio.IN)

SensorInit()
r = Rotate()
a = Auger()
s = Spoon()

while gpio.input(spoon_home_pin) == 0:
    s.pulseSp(False, 1)

while gpio.input(rotate_home_pin) == 0:
    r.pulseRot(False, 1)
r.pulseRot(True, 5)

s.pulseSp(True, 5)
r.pulseRot(False, 3)
r.pulseRot(True, 8)

while gpio.input(spoon_home_pin) == 0:
    s.pulseSp(False, 1)

s.pulseSp(True, 2)

while gpio.input(chute_pin) == 0:
    a.pulseAug(False, 5)
    a.pulseAug(True, 1)

s.pulseSp(True, 10)
