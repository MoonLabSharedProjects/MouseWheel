import RPi.GPIO as GPIO
import datetime, threading, Queue, time, serial, math, csv
from hx711 import HX711

GPIO.setwarnings(False)
print "Calibrating weight sensor"
hx = HX711(9,11)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(2363.2)
hx.reset()
hx.tare()
print "Weight Sensor Calibrated"

header = ['Time', 'Interval', 'Distance', 'Weight', 'RFID', 'Average int Speed']

with open('wheeldata.csv','w') as newFile:
    newFileWriter = csv.DictWriter(newFile, header)
    newFileWriter.writeheader()

    lst = []
    weight = []
    RFID = []

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

    class Logging:
        def __init__(self):
            self.running = True
            self.port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.1)
            global int_no
            int_no = 0

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

        def timer(self):
            global start_1
            start_1 = 0
            while True:
                time.sleep(1)
                start_1 += 1
                print start_1

        def results(self):
            global start_1
            if start_1 > 3 and len(lst) > 2:
                print "yep"
                dist = (len(lst) / 20) * (11 * math.pi)
                # stop RFID and Weight threads
                ResultDict = {'Time': lst[0],
                              'Interval': int_no,
                              'Distance': dist,
                              'Weight': 4,
                              'RFID': 5,
                              'Average int Speed': 6}
                newFileWriter.writerow(ResultDict)
                print ResultDict
                int_no += 1
                del lst[:]
                del weight[:]
                del RFID[:]
            else:
                pass

        def run(self):
            global int_no #the mouse-run session
            global q #Timestamps coming from optoswitch break
            global start_1
            threading.Thread(target=self.timer).start()
            while self.running:
                while q.empty() == False:
                    #take timestamp, put it in list
                    item = q.get()
                    lst.append(item)
                    print lst
                    q.task_done()
                    start_1 = 0
                    self.results()
                    #start weight and RFID threads, take the items which the function returns
                    # and put them in weight, and RFID lists.


    def main():
        Interrupt()
        L = Logging()
        LT = threading.Thread(target=L.run, args=())
        LT.start()

    if __name__ == "__main__":
        q = Queue.Queue()
        main()

