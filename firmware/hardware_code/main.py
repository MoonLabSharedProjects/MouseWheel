#!/usr/bin/python
import RPi.GPIO as GPIO
from pymongo import MongoClient
import datetime, threading, Queue, time, sys
from hx711 import HX711

client = MongoClient("mongodb://sotiris:Ars3n4l123@ds019143.mlab.com:19143/wheel")
#client = MongoClient("mongodb://192.168.2.6/mousewheel")
db = client.wheel
session = db.dataset
file_name = time.strftime("%Y_%m_%d_%H%M")
print "Logfile name: " + file_name " created..."

print "Calibrating weight sensor..."
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
    def event_callback(self, channel):
        global q
        t = datetime.datetime.now()
        q.put(t)

class Weight:
    def __init__(self):
        self.running = True
    def run(self):
        global averageq
        weightlist = []
        while self.running:
            weight_int = intervalq.get()
            while weight_int > datetime.timedelta(seconds=3):
                unloaded = hx.get_weight(5)
                hx.power_down()
                hx.power_up()
                weightlist.append(unloaded)
                aver_unloaded_weights = float(sum(weightlist)) / len(weightlist)
                if len(weightlist) > 20:
                    weightlist.pop(0)
                rounded_avg = round(aver_unloaded_weights, 3)
                averageq.put(rounded_avg)
                time.sleep(0.5)
            else:
                intervalq.task_done()
                # pull weight information when the interrupts aren't happening, average last 10 readings
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

    def weightloaded(self):
        self.running = True
        global averageq
        if averageq.empty() == False:
            roll_avg = averageq.get()

            # pull weight informaiton when the interrups are happening
            # return current weight reading - average of unloaded weight
            loadedweight = hx.get_weight(5)
            hx.power_down()
            hx.power_up()
            weight = loadedweight - roll_avg

            print "actual:" + str(loadedweight)
            print "rolling average: " + str(roll_avg)
            print "adjusted weight: " + str(weight)
            averageq.task_done()
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
                    intervalq.put(d)
                    if d > datetime.timedelta(seconds=3):
                        int_no = int_no + 1
                        session.insert({'session_id': file_name,
                                        'interval_no': int_no,
                                        'timestamp': [],
                                        'weight': [],})
                    else:
                        session.update({'interval_no': int_no}, {'$push': {'timestamp': item, 'weight': self.weightloaded()}})
                    list.pop(0)
                q.task_done()


def main():
    while True:
        try:
            L = Logging()
            w = Weight()
            WeightClass = threading.Thread(target=w.run, args=())
            LT = threading.Thread(target=L.run, args=())
            Interrupt()
            LT.start()
            WeightClass.start()

        except KeyboardInterrupt:
            print "Main interrupt handled. Now terminating logging"
            print "Cleaning GPIO..."
            GPIO.cleanup()
            print "Cleaned"
            sys.exit()

if __name__ == "__main__":
    q = Queue.Queue()
    main()
