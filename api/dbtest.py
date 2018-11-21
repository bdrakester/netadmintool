#!/usr/local/bin/python3
# Used to test database functions, not part of application

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from configparser import ConfigParser
from database import NetAdminToolDB
#from flask import jsonify

nadb = NetAdminToolDB('netadminapi.conf')
#db = NetAdminToolDB('tests.conf')
#dev = db.get_device(12)
#db.create_tables()
#db.add_device('TEST-firewall1', '2.2.2.2', 1,
#    '9.8', 'sn7890', 'Boston', 'Rack 1', 'Serial 2',
#    'NGFW', 'Notes for firewall1')
#device = db.get_device()
#db = NetAdminToolDB('tests.conf')
#self.db.execute("SELECT id FROM users WHERE  username='adminuser' AND password='password2')
config = ConfigParser()
config.read("netadminapi.conf")

dbuser = config['DATABASE']['dbusername']
dbpass = config['DATABASE']['dbpassword']
dbhost = config['DATABASE']['hostname']
dbport = config['DATABASE']['port']

connString = f"postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/netadmintool"
engine = create_engine(connString)
db = scoped_session(sessionmaker(bind=engine))

#name='Test501'
#type='TestType'
#description='Test description'

#result = db.execute("INSERT INTO devices (name, device_type, description) \
#                        VALUES (:name, :type, :description) RETURNING id",
#                        {'name': name, 'type': type, 'description': description})
#db.commit()

#id = result.fetchone().id

#devices = db.execute("SELECT * FROM devices").fetchone()
#print(devices)
#myDB = NetAdminToolDB('netadminapi.conf')
#myDB.add_device('router2','ios_router','My second router')

#myDevice = myDB.get_device(1)
#allDevices = myDB.get_device()

#deviceList = []
#for device in allDevices:
#    deviceList.append({'id': device.id, 'name': device.name})
