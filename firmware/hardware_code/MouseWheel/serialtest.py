import serial, time

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.1)

def serial_1():
    a = port.readline()
    if len(a) < 15  or a == "?1\r":
        return "No Tag"
    else:
        return str(a)

while True:
    print serial_1()
    time.sleep(1)