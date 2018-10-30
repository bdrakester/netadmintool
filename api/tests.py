# tests.py
# Unit tests for database and api
# Needs tests.conf file for database connection information

## TODO - testing api currently connects to production database.  How to
## get it to use the test database?  Pass the database file name as parameter
## somehow

import os
import unittest

from database import NetAdminToolDB
from application import create_test_app

# Contains test database connection information
CONFIG_FILE = 'tests.conf'

class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #print('Running setUpClass ...')
        self.db = NetAdminToolDB(CONFIG_FILE)


    def setUp(self):
        print('Running setUp ...')
        self.db.create_tables()
        self.db.add_device('firewall1', '2.2.2.2', 'cisco_asa', 'Cisco',
            'ASA 5525-X', '9.8', 'sn7890', 'Boston', 'Rack 1', 'Serial 2',
            'NGFW', 'Notes for firewall1')
        self.db.add_device('switch1', '3.3.3.3', 'cisco_sg', 'Cisco', 'SG500',
            '3.1.4', 'sn9876', 'Boston', 'Rack 2', 'Serial 3', 'Core switch',
            'Notes for switch1')

        api = create_test_app()
        self.client = api.test_client()



    def test_add_device(self):
        """ Test adding a device to the database """

        print('Running test_add_device ... ')
        res = self.db.add_device('router1','1.1.1.1','cisco_ios','Cisco','2900',
        '15.4','sn1234','Boston','Rack 1','Serial 1','Internet router',
        'Notes for router1')

        self.assertIsInstance(res,int)

    def test_get_device_no_args(self):
        """ Test get_device with no arguments """

        print('Running test_get_device_no_args ... ')
        res = self.db.get_device()

        self.assertEqual(len(res),2)

    def test_get_device(self):
        """ Test get_device with id argument """

        print('Running test_get_device ...')
        allDevices = self.db.get_device()
        res = self.db.get_device(allDevices[0].id)

        self.assertNotEqual(res,None)

    def test_get_device_name(self):
        """ Test getting a device by name """

        print('Running test_get_device_name ...')
        res = self.db.get_device_name('firewall1')
        self.assertEqual(res.device_type,'cisco_asa')

    def test_update_device(self):
        """ Test updating a device """
        print('Running test_update_device ...')
        device = self.db.get_device_name('firewall1')
        self.db.update_device(device.id, serial_number='SS112233')
        res = self.db.get_device(device.id).serial_number

        self.assertEqual(res,'SS112233')

    def test_delete_device(self):
        """ Test deleting a device """

        print('Running test_delete_device')
        device = self.db.get_device_name('firewall1')
        self.db.delete_device(device.id)

        res = self.db.get_device(device.id)

        self.assertEqual(res,None)

    def test_api_devices(self):
        """ Test api get all devices """

        print('Running test_api_devices')
        res = self.client.get('/api/devices')
        json_data = res.get_json()
        for device in json_data['devices']:
            print(f"device = {device}")
        self.assertEqual(res.status_code, 200)




if __name__ == "__main__":
    unittest.main()
