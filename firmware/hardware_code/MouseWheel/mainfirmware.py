
import RPi.GPIO as GPIO
import time, sys, serial, math
from time import sleep
from hx711 import HX711
from uuid import getnode as get_mac

mac = get_mac()
file_name = "wheel_" + time.strftime("%d_%m_%Y_%H%M")
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
times = []
rpm1 = []
blixed = [1, 2, 3]
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=20000)
units = " grams"
GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback)
hx = HX711(9, 11)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(2363.2)
hx.reset()
hx.tare()

sleep(2)

class AHF_TagReader:
    def __init__(self, serialPort, timeOutSecs = -1):
        # initialize serial port
        self.serialPort = None

        try:
            if (timeOutSecs < 0):
                self.serialPort = serial.Serial(str (serialPort), baudrate=9600)
            else:
                self.serialPort = serial.Serial(str (serialPort), baudrate=9600, timeout=timeOutSecs)
        except IOError as anError:
            print ("Error initializing TagReader serial port.." + str (anError))
            raise anError
        if (self.serialPort.isOpen() == False):
            self.serialPort.open()
        self.serialPort.flushInput()

    def readTag (self):
        rawTag = self.serialPort.readline() #consumes an entire line up to CR LF or times out and consumes not$
        if rawTag.__len__() ==0: # the read timed out, so return 0
            0
        elif rawTag.__len__() < 15: #this should never happen
            self.serialPort.flushInput()
            raise IOError
        self.serialPort.read (1)
        return rawTag

def cleanAndExit():
    print "Cleaning and closing..."
    GPIO.cleanup()
    print "Program closed"
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
    val = hx.get_weight(3)
    r_val = round(val, 1)
    hx.power_down()
    hx.power_up()
    if r_val < 0:
        return 0
    else:
        return math.fabs(r_val))

L = []
serialPort = '/dev/ttyAMA0'
tagReader = AHF_TagReader(serialPort, timeOutSecs=0.1)

while True:
    with open(file_name + ".csv", 'w') as csvfile:
        fieldnames = ['timestamp', 'mac_address', 'RPM', 'Weight', 'RFID', 'interval']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        try:
            interval = 1
            if weight() > 0 or readings_1() > 0:
                writer.writerow({'timestamp': time.strftime("%d_%m_%Y_%H%M"), 'mac_address': mac, 'RPM': readings_1(),
                                 'Weight': weight(), 'RFID': serial()}, 'interval': interval)
                interval += 1
                time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

