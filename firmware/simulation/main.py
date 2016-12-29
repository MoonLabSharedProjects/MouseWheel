#!/usr/bin/python
"""import RPi.GPIO as GPIO"""
from pymongo import MongoClient
import datetime, threading, Queue, time, random, sys, curses, math

print "Initiating..."
client = MongoClient()
db = client.testwheel
session = db.dataset
file_name = time.strftime("%Y_%m_%d_%H%M")
#print "Logfile name: " + file_name+".log" + " created..."
#logging.basicConfig(filename=file_name+".log",level=logging.DEBUG)
stdscr = curses.initscr()
stdscr.addstr(1, 4, "RodentRunner Simulation V1", curses.A_BOLD)
stdscr.addstr(5, 4, "Weight Readings...", curses.A_BOLD)


class Interrupt:
    def __init__(self):
        global q
        for i in range(300):
            t = datetime.datetime.now()
            q.put(t)
            r = random.randrange(1,5)
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
            while weight_int > 3:
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
            loadedweight = random.randrange(26, 30)
            weight = loadedweight - roll_avg

            stdscr.addstr(7, 4, "Raw weight (grams): ")
            stdscr.addstr(7, 35, str(loadedweight), curses.A_BOLD)
            stdscr.addstr(8, 4, "Average (grams): ")
            stdscr.addstr(8, 35, str(roll_avg), curses.A_BOLD)
            stdscr.addstr(9, 4, "Adjusted weight (grams): ")
            stdscr.addstr(9, 35, str(weight), curses.A_BOLD)

            stdscr.refresh()
            averageq.task_done()
            return weight

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
                    e = d.total_seconds()
                    intervalq.put(e)
                    #print "time between last two timestamps " + str(d)
                    if e > 3:
                        int_no += 1
                        #print "interval number: " + str(int_no)
                        session.insert({'session_id': file_name,
                                        'interval_no': int_no,
                                        'timestamp': [],
                                        'weight': [], })
                        #print "a new interval has now started"
                        stdscr.addstr(3, 4, "Current speed (KPH): ")
                        stdscr.addstr(3, 35, "0             ", curses.A_BOLD)
                        stdscr.refresh()
                    else:
                        session.update({'interval_no': int_no},
                                       {'$push': {'timestamp': item, 'weight': self.weightloaded()}})
                        # print "this timestamp, " + str(item) + " was added to this interval: " + str(int_no)
                        diameter = math.pi * 10
                        cs = diameter / e
                        kph = cs * 0.036
                        rounded_kph = round(kph, 3)
                        stdscr.addstr(3, 4, "Current speed (KPH): ")
                        stdscr.addstr(3, 35, str(rounded_kph), curses.A_BOLD)
                        stdscr.refresh()

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
