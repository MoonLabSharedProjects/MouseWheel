import time, csv, random
from uuid import getnode as get_mac

file_name = time.strftime("%d_%m_%Y_%H%M")
mac = get_mac()

def serial():
    return "No tag"

def rpm():
    a = random.randint(0, 10)
    return a

def weight():
    b = random.randint(0, 30)
    return b

with open(file_name + ".csv", 'w') as csvfile:
    fieldnames = ['timestamp', 'mac_address', 'RPM', 'Weight', 'RFID', 'interval']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    print "header created"
    while True:
        x = readings_1()
        while x > 0:
            writer.writerow({'timestamp': time.strftime("%d_%m_%Y_%H%M"), 'mac_address': mac, 'RPM': x, 'Weight': weight(), 'RFID': serial()})
            time.sleep(0.1)

