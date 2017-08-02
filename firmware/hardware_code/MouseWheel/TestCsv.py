import csv, time

file_name = time.strftime("%d_%m_%Y_%H%M")
with open(file_name+".csv", 'w') as csvfile:
    fieldnames = ['timestamp', 'first_name', 'last_name', 'mac_address']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    name = 0
    number = 0
    for i in range(30):
        name += 1
        number += 2
        writer.writerow({'timestamp': time.strftime("%d_%m_%Y_%H%M"), 'first_name': name, 'last_name': number, 'mac_address': "90909"})
