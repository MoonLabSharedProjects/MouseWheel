import serial

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=20000)

def serial():
    a = port.readline(1)
    if a.__len__() == 0:
        return 0
    else:
        return a

while True:
    print serial()
