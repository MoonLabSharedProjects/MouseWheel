#!/usr/bin/python
import RPi.GPIO as GPIO
from pymongo import MongoClient
import datetime, threading, Queue, time, sys, serial, math
from hx711 import HX711

file_name = time.strftime("%d_%m_%Y_%H%M")
print "Connecting to db"
client = MongoClient("mongodb://10.0.0.1:37018/wheel")
print "Connected to db"
db = client.wheel
session = db.dataset
session.insert({'status': "started"})
GPIO.setwarnings(False)
print "Calibrating weight sensor"
hx = HX711(9,11)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(2363.2)
hx.reset()
hx.tare()
print "Weight Sensor Calibrated"

class Interrupt:
    def __init__(self):
	    GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(5, GPIO.FALLING, callback=self.event_callback)
    def event_callback(self):
        global q
        t = datetime.datetime.now()
        q.put(t)

class Logging:
    def __init__(self):
        self.running = True
        self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.1)
        global int_no
        int_no = 0
        session.insert({'session_id': file_name,
                        'interval_no': int_no,
                        'timestamp': [],
                        'weight': [],
                        'RFID': []})
#initialises the first MongoDB collection with default document
#models weight data, this function is called everytime an "interrupt" happens
    def weight(self):
        val = hx.get_weight(1)
        r_val = round(val, 1)
        return math.fabs(r_val)

    def tare(self):
        hx.tare()

    def rfid(self):
        self.port.write("RSD\r")
        time.sleep(0.05)
        a = port.readline()
        if len(a) < 15 or a == "?1\r":
            return "No Tag"
        else:
            return str(a)

    def run(self):
        global int_no
        global q
        list = []
        while self.running:
            if q.empty() == False:
                item = q.get()
                list.append(item)
                if len(list) > 2:
                    a = len(list)
                    b = list[a-2]
                    c = list[a-1]
                    d = c - b
                    intervalq.put(d)
                    if d > datetime.timedelta(seconds=3):
                        int_no = int_no + 1
                        session.insert({'session_id': file_name,
                                        'interval_no': int_no,
                                        'timestamp': [],
                                        'weight': [],
                                        'RFID': []})
                        self.tare()
                    else:
                        session.update({'interval_no': int_no}, {'$push': {'timestamp': item, 'weight': self.weight(), 'RFID': self.rfid()}})
                    list.pop(0)
                q.task_done()


def main():
    Interrupt()
    L = Logging()
    LT = threading.Thread(target=L.run, args=())
    LT.start()

if __name__ == "__main__":
    q = Queue.Queue()
    main()

