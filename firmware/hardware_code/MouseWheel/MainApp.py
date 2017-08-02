import RPi.GPIO as GPIO
import time, sys, serial, math, csv
from hx711 import HX711
from uuid import getnode as get_mac
file_name = time.strftime("%d_%m_%Y_%H%M")
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
mac = get_mac()
times = []
rpm1 = []
blixed = [1, 2, 3]
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.1)

def serial():
    port.write("RSD\r")
    time.sleep(0.05)
    a = port.readline()
    if len(a) < 15  or a == "?1\r":
        return "No Tag"
    else:
        return str(a)

def cleanAndExit():
#    print "Cleaning and closing..."
    GPIO.cleanup()
#    print "Program closed"
    sys.exit()

def my_callback(channel):
    global times
    global rpm1
    a = time.time()
    times.append(a)
    if len(times) > 2:
        b = times[1] - times[0]
        c = b * 20
        rpm = 60 / c
        del times[0]
        rpm1.append(round(rpm, 1))

def readings_1():
    if len(rpm1) > 2:
        x = blixed[len(blixed) - 1]
        y = blixed[len(blixed) - 2]
        if x == y:
            blixed.append(rpm1[len(rpm1) - 1])
            del blixed[0]
            return 0
        else:
            blixed.append(rpm1[len(rpm1) - 1])
            del blixed[0]
            return rpm1[len(rpm1) - 1]

    else:
        return 0

def weight():
    val = hx.get_weight(1)
    r_val = round(val, 1)
    return math.fabs(r_val)

GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback)
print "Scales calibrating..."
hx = HX711(9, 11)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(2363.2)
hx.reset()
hx.tare()
print "Calibrated"

while readings_1() > 0 and weight() > 0:
    print "Mouse running, waiting to initialise...."
    time.sleep(60)
print "initiating..."

with open("wheeldata/" + file_name + ".csv", 'w') as csvfile:
    fieldnames = ['timestamp', 'mac_address', 'RPM', 'Weight', 'RFID']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    print "header created"
    print "intial speed: " + str(readings_1())
    print "initial weight: " + str(weight())
    while True:
        try:
            writer.writerow(
                {'timestamp': time.strftime("%d_%m_%Y_%H%M"), 'mac_address': mac, 'RPM': readings_1(), 'Weight': weight(),
                 'RFID': serial()})
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
