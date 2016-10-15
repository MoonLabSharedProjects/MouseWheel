#!/usr/bin/python
import RPi.GPIO as GPIO
from pymongo import MongoClient
import datetime, threading, Queue, time, logging, sys
from hx711 import HX711

client = MongoClient("mongodb://sotiris:#@ds019143.mlab.com:19143/wheel")
db = client.wheel
collection = db.data_wheel
file_name = time.strftime("%Y_%m_%d_%H%M")
print "Logfile name: " + file_name+".log" + " created..."
logging.basicConfig(filename=file_name+".log",level=logging.DEBUG)

print "Calibrating weight sensor"
hx = HX711(9,11)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(2104)
hx.reset()
hx.tare()
print "Weight calibration complete"

class Interrupt:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.event_callback, bouncetime=200)
    def event_callback(self, channel):
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
                        'weight': [],})
#initialises the first MongoDB collection with default documents
    def weight(self):
        self.running = True
        weight = hx.get_weight(5)
        hx.power_down()
        hx.power_up()
        return weight
#models weight data, this function is called everytime an "interrupt" happens
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
                    if d > datetime.timedelta(seconds=3):
                        int_no = int_no + 1
                        print "interval number: " + str(int_no)
                        session.insert({'session_id': file_name,
                                        'interval_no': int_no,
                                        'timestamp': [],
                                        'weight': [],})
                    else:
                        session.update({'interval_no': int_no}, {'$push': {'timestamp': item, 'weight': self.weight()}})
                    list.pop(0)
                q.task_done()


def main():
        LT = threading.Thread(target=L.run, args=())
        L = Logging()
        LT.start()
        Interrupt()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            L.stop()
            print "Main interrupt handled. Now terminating logging"
            print "Cleaning GPIO..."
            GPIO.cleanup()
            print "Cleaned"
            sys.exit()



if __name__ == "__main__":
    q = Queue.Queue()
    main()
