# tests.py
# Unit tests for database and api
# Needs tests.conf file for database connection information

## TODO - testing api currently connects to production database.  How to
## get it to use the test database?  Pass the database file name as parameter
## somehow
## Think I have this working now - in application.py set database object
## app.config['DATABASE'], still need to update rest of application.py to
## look there for the application database object

import os
import unittest

from database import NetAdminToolDB as DB
from application import app, netAdminToolDB

# Contains test database connection information
CONFIG_FILE = 'tests.conf'

class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #print('DEBUG: test.py Running setUpClass ...')
        self.db = DB(CONFIG_FILE)


    def setUp(self):
        #print('DEBUG: tests.py - Running setUp ...')
        self.db.create_tables()
        self.db.add_device('TEST-firewall1', '2.2.2.2', 'cisco_asa', 'Cisco',
            'ASA 5525-X', '9.8', 'sn7890', 'Boston', 'Rack 1', 'Serial 2',
            'NGFW', 'Notes for firewall1')
        self.db.add_device('TEST-switch1', '3.3.3.3', 'cisco_sg', 'Cisco', 'SG500',
            '3.1.4', 'sn9876', 'Boston', 'Rack 2', 'Serial 3', 'Core switch',
            'Notes for switch1')

        app.config['DATABASE'] = DB(CONFIG_FILE)
        #print(f"DEBUG tests.py setUP() app.config[DATABASE] = {app.config['DATABASE'].dbname}")
        self.client = app.test_client()
        self.client.testing = True




    def test_add_device(self):
        """ Test adding a device to the database """

        #print('Running test_add_device ... ')
        res = self.db.add_device('TEST-router1','1.1.1.1','cisco_ios','Cisco','2900',
        '15.4','sn1234','Boston','Rack 1','Serial 1','Internet router',
        'Notes for router1')

        self.assertIsInstance(res,int)

    def test_get_device_no_args(self):
        """ Test get_device with no arguments """

        #print('Running test_get_device_no_args ... ')
        res = self.db.get_device()

        self.assertEqual(len(res),2)

    def test_get_device(self):
        """ Test get_device with id argument """

        #print('Running test_get_device ...')
        allDevices = self.db.get_device()
        res = self.db.get_device(allDevices[0].id)

        self.assertNotEqual(res,None)

    def test_get_device_name(self):
        """ Test getting a device by name """

        #print('Running test_get_device_name ...')
        res = self.db.get_device_name('TEST-firewall1')
        self.assertEqual(res.device_type,'cisco_asa')

    def test_update_device(self):
        """ Test updating a device """
        #print('Running test_update_device ...')
        device = self.db.get_device_name('TEST-firewall1')
        self.db.update_device(device.id, serial_number='SS112233')
        res = self.db.get_device(device.id).serial_number

        self.assertEqual(res,'SS112233')

    def test_delete_device(self):
        """ Test deleting a device """

        #print('Running test_delete_device')
        device = self.db.get_device_name('TEST-firewall1')
        self.db.delete_device(device.id)

        res = self.db.get_device(device.id)

        self.assertEqual(res,None)

    def test_api_devices(self):
        """ Test api get all devices """

        #print('Running test_api_devices')
        res = self.client.get('/api/devices')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json_data['devices']),2)


if __name__ == "__main__":
    unittest.main()
