#!/usr/bin/python
import RPi.GPIO as GPIO
from pymongo import MongoClient
import datetime, threading, Queue, time, sys
from hx711 import HX711

print "Connecting to db"
client = MongoClient("mongodb://192.168.2.1/wheel")
print "Connected to db"
db = client.wheel
session = db.dataset
session.insert({'status': "started"})
file_name = time.strftime("%Y_%m_%d_%H%M")
print "Logfile name: " + file_name+".log" + " created..."


print "Calibrating weight sensor"
hx = HX711(9,11)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(1052)
hx.reset()
hx.tare()
print "Weight Sensor Calibrated"

class Interrupt:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.event_callback, bouncetime=200)
    def event_callback(self):
        global q
        t = datetime.datetime.now()
        q.put(t)

class Logging:
    def __init__(self):
        self.running = True

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
        port.write("RSD\r")
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
    while True:
        try:
            L = Logging()
            LT = threading.Thread(target=L.run, args=())
            Interrupt()
            LT.start()

        except KeyboardInterrupt:
            print "Main interrupt handled. Now terminating logging"
            print "Cleaning GPIO..."
            GPIO.cleanup()
            print "Cleaned"
            sys.exit()

if __name__ == "__main__":
    q = Queue.Queue()
    main()
