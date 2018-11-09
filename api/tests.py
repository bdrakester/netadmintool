# tests.py
# Unit tests for database and api
# Needs tests.conf file for database connection information

import os
import unittest

from database import NetAdminToolDB as DB
from application import app

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
        self.db.add_device('TEST-firewall1', '2.2.2.2', 'Cisco',
            'ASA 5525-X', '9.8', 'sn7890', 'Boston', 'Rack 1', 'Serial 2',
            'NGFW', 'Notes for firewall1')
        self.db.add_device('TEST-switch1', '3.3.3.3', 'Cisco', 'SG500',
            '3.1.4', 'sn9876', 'Boston', 'Rack 2', 'Serial 3', 'Core switch',
            'Notes for switch1')

        app.config['DATABASE'] = DB(CONFIG_FILE)
        #print(f"DEBUG tests.py setUP() app.config[DATABASE] = {app.config['DATABASE'].dbname}")
        self.client = app.test_client()
        self.client.testing = True


    def test_add_device(self):
        """ Test adding a device to the database """

        #print('Running test_add_device ... ')
        res = self.db.add_device('TEST-router1','1.1.1.1', 'Cisco','2900',
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
        self.assertEqual(res.serial_number,'sn7890')

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

    def test_api_get_device(self):
        """ Test api get device id 1 """

        res = self.client.get('/api/devices/1')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['device']['id'],1)

    def test_api_update_device(self):
        """ Test api update device id 1 """

        res = self.client.put('/api/devices/1', json={
            'description':'Updated Description of device 1'})
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['device']['description'],
            'Updated Description of device 1')

    def test_api_add_device(self):
        """ Test api adding a device """
        newDevice = {'name': 'NewRouter2', 'ip_addr': '192.168.1.2',
            'make':'test make', 'model':'test model',
            'sw_version': '1337', 'serial_number':'snTEST',
            'datacenter':'Test DC', 'location': 'Test Location',
            'console': 'Test 1', 'description':'Desc of NewRouter2 ',
            'notes':'Notes re: NewRouter2'}

        res = self.client.post('/api/devices', json=newDevice)
        json_data = res.get_json()
        self.assertEqual(res.status_code,201)
        self.assertEqual(json_data['device']['sw_version'], '1337')


    def test_api_delete_device(self):
        """ Test api delete device id 1 """

        res = self.client.delete('/api/devices/1')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/api/devices/1')
        self.assertEqual(res.status_code, 404)

    def test_api_get_device_name(self):
        """ Test api get device by name query string """

        res = self.client.get('/api/devices?name=TEST-firewall1')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['devices'][0]['notes'],'Notes for firewall1')


if __name__ == "__main__":
    unittest.main()
