from __future__ import division
import RPi.GPIO as GPIO
import datetime, threading, Queue, time, serial, math, csv
from hx711 import HX711
import numpy as np
GPIO.setwarnings(False)

def most_frequent_first(events):
    most = {}
    rfids = set(events)
    if len(events) > 1:
        for i in rfids:
            n = i.rstrip()
            count = events.count(i)
            most[n] = count
        v=list(most.values())
        k=list(most.keys())
        return k[v.index(max(v))]
    else:
        return "No Tag"

file_name = time.strftime("%d_%m_%Y_%H%M")
print ("Calibrating weight sensor")
hx = HX711(9,11)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(2363.2)
hx.reset()
hx.tare()
print ("Weight Sensor Calibrated")
diam = 11 * math.pi
header = ['Time', 'Interval', 'Distance', 'Weight', 'RFID', 'Average int Speed']

with open('wheeldata_'+file_name+'.csv','w') as newFile:
    newFileWriter = csv.DictWriter(newFile, header)
    newFileWriter.writeheader()

lst = []
weightlist = []
weight_1 = []
rfid_1 = []

class Interrupt:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(5, GPIO.FALLING, callback=self.event_callback)

    def event_callback(self, channel):
        global q
        t = datetime.datetime.now()
        q.put(t)

class MouseInfo:
    def __init__(self, info, capturetime):
        self.info = info
        self.capturetime = capturetime

class Logging:
    def __init__(self):
        self.running = True
        self.port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.1)
        global int_no
        int_no = 0

    def weight(self):
        while True:
            val = hx.get_weight(1)
            r_val = round(val, 1)
            time.sleep(1)
            weightlist.append(MouseInfo(r_val, time.time()))
            if len(weightlist) > 6:
                weightlist.pop(0)

    def tare(self):
        hx.tare()

    def rfid(self):
        text = ""
        while True:
            s = self.port.read(1)
            if (s != ""):
                text = text + str(s)
                if (ord(s) == 13):
                    rf.put(text)
                    print (text)
                    text = ""

    def results(self):
        global int_no
        dist = len(lst)/20 * diam
        tme = lst[len(lst)-1] - lst[0]
        with open('wheeldata_'+file_name+'.csv','a') as newFile:
            newFileWriter = csv.DictWriter(newFile, header)
            ResultDict = {'Time': lst[0],
                          'Interval': int_no,
                          'Distance': round(dist, 1),
                          'Weight': round(np.median(weight_1), 1),
                          'RFID': most_frequent_first(rfid_1),
                          'Average int Speed': round(dist/tme.total_seconds(), 1)}
            newFileWriter.writerow(ResultDict)
        print (ResultDict)
#        print (weight_1)
        #print(rfid_1)
        int_no += 1
        self.tare()
        del lst[:]
        del weight_1[:]
        del rfid_1[:]

    def run(self):
        global int_no #the mouse-run session
        global q #Timestamps coming from optoswitch break
        threading.Thread(target=self.weight).start()
        threading.Thread(target=self.rfid).start()
        current = time.time()
        while self.running:
            elapsed = time.time() - current
            if len(lst) > 2 and elapsed > 3:
                if len(weightlist) > 0:
                    s = weightlist.pop()
                    if s.info < 5:
                        self.results()
            while q.empty() == False:
                current = time.time()
                item = q.get()
                lst.append(item)
                q.task_done()
                if rf.empty() == False:
                    rfdata = rf.get()
                    rfid_1.append(rfdata)
                elif len(rfid_1) == 0:
                    rfid_1.append("No Tag")
                else:
                    rfid_1[0] = "No Tag"
                if len(weightlist) > 0:
                    s = weightlist.pop()
                    k = current - s.capturetime
                    if k < 1:
                        weight_1.append(s.info)

def main():
    Interrupt()
    L = Logging()
    LT = threading.Thread(target=L.run, args=())
    LT.start()

if __name__ == "__main__":
    q = Queue.Queue()
    rf = Queue.Queue()
    main()






