#!/usr/local/bin/python3
# Used to test database functions, not part of application

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from configparser import ConfigParser
from database import NetAdminToolDB
from flask import jsonify

#config = ConfigParser()
#config.read("config.txt")

#dbuser = config['DATABASE']['dbusername']
#dbpass = config['DATABASE']['dbpassword']
#dbhost = config['DATABASE']['hostname']
#dbport = config['DATABASE']['port']

#connString = f"postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/netadmintool"
#engine = create_engine(connString)
#db = scoped_session(sessionmaker(bind=engine))

#devices = db.execute("SELECT * FROM devices").fetchone()
#print(devices)


myDB = NetAdminToolDB('netadminapi.conf')
#myDB.add_device('router2','ios_router','My second router')

myDevice = myDB.get_device(1)
#allDevices = myDB.get_device()

#deviceList = []
#for device in allDevices:
#    deviceList.append({'id': device.id, 'name': device.name})
