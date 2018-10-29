import csv
from database import NetAdminToolDB

db = NetAdminToolDB("netadminapi.conf")

def main():
    print('Net Admin Tool Database Import')
    file = open('devices.csv')
    reader = csv.reader(file)
    for name, ip_addr, type, make, model, sw_version, serial, datacenter, \
        location, console, descr, notes in reader:
        db.add_device(name, ip_addr, type, make, model, sw_version, serial,
            datacenter, location, console, descr, notes)
        print(f'Imported name = {name}  ip_addr = {ip_addr}')

if __name__ == '__main__':
    main()
