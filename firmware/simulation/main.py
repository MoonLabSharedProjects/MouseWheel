#!/usr/bin/python
"""import RPi.GPIO as GPIO"""
from pymongo import MongoClient
import datetime, threading, Queue, time, logging, random

client = MongoClient("mongodb://localhost/mousewheel")
print "Connection to database successful..."
db = client.wheel
session = db.dataset
file_name = time.strftime("%Y_%m_%d_%H%M")
print "Logfile name: " + file_name+".log" + " created..."
#logging.basicConfig(filename=file_name+".log",level=logging.DEBUG)

class Interrupt:
    def __init__(self):
        global q
        for i in range(300):
            t = datetime.datetime.now()
            q.put(t)
            r = random.randrange(0,4)
            time.sleep(r)
#places a timestamp into queue "q", sleeps for a random amount of seconds between 1-9, then repeats 300 times

class Logging:
    def __init__(self):
        self.running = True
        global int_no
        int_no = 0
        session.insert({'session_id': file_name,
                        'interval_no': int_no,
                        'timestamp': [],
                        'weight': [],})
#initialises the first collection with default documents
    def weight(self):
        self.running = True
        weight = random.randrange(24,35)
        return weight

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
                    print "time between last two timestamps " + str(d)
                    if d > datetime.timedelta(seconds=3):
                        int_no = int_no + 1
                        print "interval number: " + str(int_no)
                        session.insert({'session_id': file_name,
                                        'interval_no': int_no,
                                        'timestamp': [],
                                        'weight': [],})
                        print "a new interval has now started"
                    else:
                        print "interval number: " + str(int_no)
                        session.update({'interval_no': int_no}, {'$push': {'timestamp': item, 'weight': self.weight()}})
                        print "this timestamp, " + str(item) + " was added to this interval: " + str(int_no)
                    list.pop(0)
                q.task_done()


def main():
        L = Logging()
        LT = threading.Thread(target=L.run, args=())
        LT.start()
        Interrupt()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print "Main interrupt handled. Now terminating logging"
            L.stop()


if __name__ == "__main__":
    q = Queue.Queue()
    main()
