#!/usr/bin/python
"""import RPi.GPIO as GPIO"""
from pymongo import MongoClient
import datetime, threading, Queue, time, logging, random, sys

client = MongoClient("mongodb://localhost/mousewheel")
print "Connection to database successful..."
db = client.testwheel
session = db.dataset
file_name = time.strftime("%Y_%m_%d_%H%M")
#print "Logfile name: " + file_name+".log" + " created..."
#logging.basicConfig(filename=file_name+".log",level=logging.DEBUG)

class Interrupt:
    def __init__(self):
        global q
        for i in range(300):
            t = datetime.datetime.now()
            q.put(t)
            r = random.randrange(0,5)
            time.sleep(r)
#places a timestamp into queue "q", sleeps for a random amount of seconds between 1-4, repeats 300 times
class Weight:
    def __init__(self):
        self.running = True
    def run(self):
        global averageq
        weightlist = []
        while self.running:
            weight_int = intervalq.get()
            while weight_int > datetime.timedelta(seconds=3):
                cool = random.randrange(-3, 6)
                weightlist.append(cool)
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
#initialises the first MongoDB collection with default document


    def weightloaded(self):
        self.running = True
        global averageq
        if averageq.empty() == False:
            roll_avg = averageq.get()

            #pull weight informaiton when the interrups are happening
            #return current weight reading - average of unloaded weight
            loadedweight = random.randrange(27, 29)
            weight = loadedweight - roll_avg

            print "actual:" + str(loadedweight)
            print "rolling average: " + str(roll_avg)
            print "adjusted weight: " + str(weight)
            averageq.task_done()
            return weight
        else:
            print ""

    #models weight data, this function is called everytime an "interrupt" happens
    def run(self):
        global int_no
        global q
        global d
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
                    print "time between last two timestamps " + str(d)
                    if d > datetime.timedelta(seconds=3):
                        int_no += 1
                        print "interval number: " + str(int_no)
                        session.insert({'session_id': file_name,
                                        'interval_no': int_no,
                                        'timestamp': [],
                                        'weight': [], })
                        print "a new interval has now started"
                    else:
                        print "interval number: " + str(int_no)
                        session.update({'interval_no': int_no}, {'$push': {'timestamp': item, 'weight': self.weightloaded()}})
                        print "this timestamp, " + str(item) + " was added to this interval: " + str(int_no)
                    list.pop(0)
                q.task_done()


def main():
    while True:
        try:
            L = Logging()
            w = Weight()
            WeightClass = threading.Thread(target=w.run, args=())
            LT = threading.Thread(target=L.run, args=())
            LT.start()
            WeightClass.start()
            Interrupt()
        except KeyboardInterrupt:
            print "Main interrupt handled. Now terminating logging"
            sys.exit()



if __name__ == "__main__":
    q = Queue.Queue()
    intervalq = Queue.Queue()
    averageq = Queue.Queue()
    main()
