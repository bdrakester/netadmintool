import csv
from database import NetAdminToolDB

db = NetAdminToolDB("netadminapi.conf")

def main():
    print('Net Admin Tool Database Import')
    file = open('devices.csv')
    reader = csv.reader(file)
    for name, ip_addr, device_type_id, sw_version, serial, datacenter, \
        location, console, descr, notes in reader:
        db.add_device(name, ip_addr, device_type_id, sw_version, serial,
            datacenter, location, console, descr, notes)
        print(f'Imported name = {name}  ip_addr = {ip_addr}')
    file.close()

    with open('users.csv') as usersFile:
        reader = csv.reader(usersFile)
        for username, password, display_name, role_name in reader:
            db.add_user(username,password,display_name,role_name)
        print(f'Imported user = {username}')

if __name__ == '__main__':
    main()
