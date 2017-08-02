import serial, time

class AHF_TagReader:
    def __init__(self, serialPort, timeOutSecs = -1):
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
        rawTag = self.serialPort.readline() #consumes an entire line up to CR LF or times out and consumes nothing at all
        if rawTag.__len__() ==0: # the read timed out, so return 0
            return 0
        elif rawTag.__len__() < 15: #this should never happen
            self.serialPort.flushInput()
            raise IOError
        self.serialPort.read (1) # to clear the ETX that comes AFTER the CR LF
        return rawTag

L = []
serialPort = '/dev/ttyAMA0'
tagReader = AHF_TagReader (serialPort, timeOutSecs = 0.1)
while True:
    p =  tagReader.readTag()
    if p != 0:
        L.append(p)
        s = L[len(L)-1]
        for i in range(10):
            time.sleep(0.1)
            print s
    else:
        print "No tag"