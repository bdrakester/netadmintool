# tests.py
# Unit tests for database and api
# Needs tests.conf file for database connection information

import os
import unittest

from database import NetAdminToolDB as DB
from application import app
#from utils import get_version_from_device

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
        self.db.add_device('TEST-firewall1', '2.2.2.2', 1,
            '9.8', 'sn7890', 'Boston', 'Rack 1', 'Serial 2',
            'NGFW', 'Notes for firewall1')
        self.db.add_device('TEST-switch1', '3.3.3.3', 3,
            '3.1.4', 'sn9876', 'Boston', 'Rack 2', 'Serial 3', 'Core switch',
            'Notes for switch1')
        self.db.add_user('TestAdmin','password','TestAdmin Display','admin')

        app.config['DATABASE'] = DB(CONFIG_FILE)
        #print(f"DEBUG tests.py setUP() app.config[DATABASE] = {app.config['DATABASE'].dbname}")
        self.client = app.test_client()
        self.client.testing = True


    ## Database tests - tests NetAdminToolDB class.
    ## Should I seperate this into a seperate Tests class from API
    def test_add_device(self):
        """ Test adding a device to the database """

        #print('Running test_add_device ... ')
        res = self.db.add_device('TEST-router1','1.1.1.1', 2,
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

    def test_get_role(self):
        """ Test getting a role by name and id from database """

        role_by_name = self.db.get_role_name('admin')
        role_by_id = self.db.get_role(role_by_name.id)

        self.assertEqual(role_by_name, role_by_id)

    def test_get_user_no_args(self):
        """ Test get_user with no arguments """
        res = self.db.get_user()

        self.assertEqual(len(res),1)

    def test_get_user(self):
        """ Test get_user by id and by name """

        user_by_name = self.db.get_user_name('TestAdmin')
        user_by_id = self.db.get_user(user_by_name.id)

        self.assertEqual(user_by_name, user_by_id)

    def test_add_user(self):
        """ Test adding a user to database """

        res = self.db.add_user('testuser','password','Test Display','admin')
        self.assertIsInstance(res,int)

        user = self.db.get_user(res)
        self.assertEqual(user.username,'testuser')

    def test_update_user(self):
        """ Test updating a user """
        #print('Running test_update_user ...')
        # Test updating Display Name
        user = self.db.get_user_name('TestAdmin')
        self.db.update_user(user.id, display_name='Updated display name')
        res = self.db.get_user(user.id).display_name
        self.assertEqual(res,'Updated display name')

        # Test updating role
        self.db.update_user(user.id, role='readonly')
        res = self.db.get_user(user.id).role_name
        self.assertEqual(res,'readonly')

        # Test updating role to non-existent role, expect
        # role to be unchanged
        self.db.update_user(user.id, role='doesNotExist')
        res = self.db.get_user(user.id).role_name
        self.assertEqual(res,'readonly')

    def test_delete_user(self):
        """ Test deleting a user """
        user = self.db.get_user_name('TestAdmin')
        self.db.delete_user(user.id)

        res = self.db.get_user(user.id)

        self.assertEqual(res,None)

    def test_authenticate_user(self):
        """ Test authenticating a user """
        res = self.db.authenticate_user('TestAdmin', 'password')
        self.assertEqual(res,True)

        res = self.db.authenticate_user('TestAdmin', 'badpassword')
        self.assertEqual(res,False)

    ### API Tests
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
            'device_type_id': 2, 'sw_version': '1337', 'serial_number':'snTEST',
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

    def test_api_users(self):
        """ Test api get all users """

        res = self.client.get('/api/users')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json_data['users']),1)

    def test_api_get_user(self):
        """ Test api get user id 1 """

        res = self.client.get('/api/users/1')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['user']['id'],1)

    def test_api_get_user_name(self):
        """ Test api get device by name query string """

        res = self.client.get('/api/users?name=TestAdmin')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['users'][0]['display_name'],'TestAdmin Display')

    def test_api_update_user(self):
        """ Test api update user id 1 """

        res = self.client.put('/api/users/1', json={
            'display_name':'New Display Name'})
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['user']['display_name'],
            'New Display Name')

    def test_api_add_user(self):
        """ Test api adding a user """
        newUser = {'username': 'NewRO_user', 'password': 'helpme!',
            'display_name':'Another RO user', 'role':'readonly'}

        res = self.client.post('/api/users', json=newUser)
        json_data = res.get_json()
        self.assertEqual(res.status_code,201)
        self.assertEqual(json_data['user']['username'], 'NewRO_user')

    def test_api_delete_user(self):
        """ Test api delete user id 1 """

        res = self.client.delete('/api/users/1')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/api/users/1')
        self.assertEqual(res.status_code, 404)

    def test_api_user_validate(self):
        """ Test api validate user credentials """

        user = {'username': 'TestAdmin', 'password': 'password'}
        res = self.client.put('api/users/validate', json=user)
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['result'], True)

        user = {'username': 'TestAdmin', 'password': 'badpassword'}
        res = self.client.put('api/users/validate', json=user)
        json_data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json_data['result'], False)

    # utils tests
    #def test_utils_cisco_asa_get_version(self):
        #""" Test CiscoASA get version """
        #device = self.db.get_device_name('TEST-firewall1')
        #res = get_version_from_device(device)
        #res = CiscoASA.get_version()
        #self.assertEqual(res,'9.2')


if __name__ == "__main__":
    unittest.main()
