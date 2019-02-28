# tests.py
# Unit tests for database and api
# Needs tests.conf file for database connection information

import os
import json
import unittest
from unittest.mock import Mock, patch
from configparser import ConfigParser

from database import NetAdminToolDB as DB
from application import app
from connectors import get_version_from_device, get_serial_from_device
from connectors import requests, netmiko

# Contains test database connection information
CONFIG_FILE = 'tests.conf'
# Path to mock device response data
FIXTURE_PATH = os.path.join('.', 'fixtures')

class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        requests.urllib3.disable_warnings()
        self.db = DB(CONFIG_FILE)
        config = ConfigParser()
        config.read(CONFIG_FILE)

    def setUp(self):
        self.db.create_tables()
        self.db.add_device('TEST-firewall1', '1.1.1.1', 1,
            '9.7', 'sn7890', 'Boston', 'Rack 1', 'Serial 2',
            'NGFW', 'Notes for firewall1')
        self.db.add_device('TEST-switch1', '3.3.3.3', 3,
            '3.1.4', 'sn9876', 'Boston', 'Rack 2', 'Serial 3', 'Core switch',
            'Notes for switch1')
        self.db.add_device('TEST-Router2', '2.2.2.2', 2,
            '12.1', 'sn456', 'Boston', 'Rack 2', 'Serial 4', 'Core Router',
            'Notes for Router2')

        self.db.add_user('TestAdmin','password','TestAdmin Display','admin')

        app.config['DATABASE'] = DB(CONFIG_FILE)
        self.client = app.test_client()
        self.client.testing = True

    def load_json_fixture(self, filename):
        """
        Load json fixture containing mock device response data. Used to
        mock Cisco ASA API responses.
        """
        file = os.path.join(FIXTURE_PATH, filename)
        with open(file) as fixture_file:
            data = json.load(fixture_file)

        return data

    def load_text_fixture(self, filename):
        """
        Load text fixture containing mock device response data. Used to
        mock Cisco IOS ssh command responses.
        """
        file = os.path.join(FIXTURE_PATH, filename)
        with open(file) as fixture_file:
            data = fixture_file.read()

        return data

    ### Database tests - tests NetAdminToolDB class.
    def test_add_device(self):
        """ Test adding a device to the database """

        res = self.db.add_device('TEST-router1','1.1.1.1', 2,
        '15.4','sn1234','Boston','Rack 1','Serial 1','Internet router',
        'Notes for router1')

        self.assertIsInstance(res,int)

    def test_get_device_no_args(self):
        """ Test get_device with no arguments """

        res = self.db.get_device()

        self.assertEqual(len(res),3)

    def test_get_device(self):
        """ Test get_device with id argument """

        allDevices = self.db.get_device()
        res = self.db.get_device(allDevices[0].id)

        self.assertNotEqual(res,None)

    def test_get_device_name(self):
        """ Test getting a device by name """

        res = self.db.get_device_name('TEST-firewall1')
        self.assertEqual(res.serial_number,'sn7890')

    def test_update_device(self):
        """ Test updating a device """

        device = self.db.get_device_name('TEST-firewall1')
        self.db.update_device(device.id, serial_number='SS112233')
        res = self.db.get_device(device.id).serial_number

        self.assertEqual(res,'SS112233')

    def test_delete_device(self):
        """ Test deleting a device """

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

        # Test updating password
        self.db.update_user(user.id,password='newpassword')
        res = self.db.authenticate_user('TestAdmin','password')
        self.assertEqual(res,False)

        res = self.db.authenticate_user('TestAdmin','newpassword')
        self.assertEqual(res,True)

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

        res = self.client.get('/api/devices')
        json_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json_data['devices']),3)

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

    @patch('application.get_version_from_device')
    def test_api_update_version_from_cisco_asa(self, mock_get_version):
        """ Test api update software version from a Cisco ASA """

        mock_get_version.return_value = '9.8(1)'

        update = {'sw_version': None, 'device_username': 'username',
            'device_password': 'password'}

        # Get the Device ID for TEST-firewall1
        res = self.client.get('/api/devices?name=TEST-firewall1')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,200)
        json_data = res.get_json()
        self.assertEqual(json_data['device']['sw_version'],"9.8(1)")

    def test_api_update_version_from_cisco_asa_no_creds(self):
        """
        Test api update software version from a Cisco ASA without credentials
        """
        update = {'sw_version': None}

        # Get the Device ID for TEST-firewall1
        res = self.client.get('/api/devices?name=TEST-firewall1')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,400)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Updates from device require credentials.')

    @patch('application.get_version_from_device')
    def test_api_update_version_from_cisco_asa_bad_creds(self, mock_get_version):
        """
        Test api update software version from a Cisco ASA with bad credentials
        """
        # If bad credentials, api response status code will not be 200,
        # CiscoASA.get_version will return None
        mock_get_version.return_value = None

        update = {'sw_version': None, 'device_username': 'username',
            'device_password': 'bad password'}

        # Get the Device ID for TEST-firewall1
        res = self.client.get('/api/devices?name=TEST-firewall1')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,404)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Unable to retrieve sw_version from device.')

    @patch('application.get_serial_from_device')
    def test_api_update_serial_from_cisco_asa(self, mock_get_serial):
        """ Test api update serial number from a Cisco ASA """

        mock_get_serial.return_value = "9APQD52LAJP"

        update = {'serial_number': None, 'device_username': 'username',
            'device_password': 'password'}

        # Get the Device ID for TEST-firewall1
        res = self.client.get('/api/devices?name=TEST-firewall1')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,200)
        json_data = res.get_json()
        self.assertEqual(json_data['device']['serial_number'],"9APQD52LAJP")

    def test_api_update_serial_from_cisco_asa_no_creds(self):
        """
        Test api update serial number from a Cisco ASA without credentials
        """
        update = {'serial_number': None}

        # Get the Device ID for TEST-firewall1
        res = self.client.get('/api/devices?name=TEST-firewall1')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,400)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Updates from device require credentials.')

    @patch('application.get_serial_from_device')
    def test_api_update_serial_from_cisco_asa_bad_creds(self, mock_get_serial):
        """
        Test api update serial number from a Cisco ASA without credentials
        """

        # If bad credentiasls, api response status code will not be 200,
        # CiscoASA.get_serial will return None
        mock_get_serial.return_value = None

        update = {'serial_number': None, 'device_username': 'username',
            'device_password': 'bad password'}

        # Get the Device ID for TEST-firewall1
        res = self.client.get('/api/devices?name=TEST-firewall1')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,404)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Unable to retrieve serial_number from device.')

    @patch('application.get_version_from_device')
    def test_api_update_version_from_cisco_ios(self, mock_get_version):
        """ Test api update software version from a Cisco IOS """

        update = {'sw_version': None, 'device_username': 'username',
            'device_password': 'password'}

        mock_get_version.return_value = '12.4(24)T6'
        # Get the Device ID for TEST-Router2
        res = self.client.get('/api/devices?name=TEST-Router2')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,200)
        json_data = res.get_json()
        self.assertEqual(json_data['device']['sw_version'],'12.4(24)T6')

    def test_api_update_version_from_cisco_ios_no_creds(self):
        """
        Test api update software version from a Cisco IOS without credentials
        """

        update = {'sw_version': None}

        # Get the Device ID for TEST-Router2
        res = self.client.get('/api/devices?name=TEST-Router2')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,400)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Updates from device require credentials.')

    @patch('application.get_version_from_device')
    def test_api_update_version_from_cisco_ios_bad_creds(self, mock_get_version):
        """
        Test api update software version from a Cisco IOS without credentials
        """

        update = {'sw_version': None, 'device_username': 'username',
            'device_password': 'bad password'}

        # get_version_from_device returns None with bad credentials
        mock_get_version.return_value = None

        # Get the Device ID for TEST-Router2
        res = self.client.get('/api/devices?name=TEST-Router2')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,404)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Unable to retrieve sw_version from device.')

    @patch('application.get_serial_from_device')
    def test_api_update_serial_from_cisco_ios(self, mock_get_serial):
        """ Test api update serial number from a Cisco IOS """

        update = {'serial_number': None, 'device_username': 'username',
            'device_password': 'password'}

        mock_get_serial.return_value = '4279256517'
        # Get the Device ID for TEST-Router2
        res = self.client.get('/api/devices?name=TEST-Router2')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,200)
        json_data = res.get_json()
        self.assertEqual(json_data['device']['serial_number'],'4279256517')

    def test_api_update_serial_from_cisco_ios_no_creds(self):
        """
        Test api update serial number from a Cisco IOS without credentials
        """

        update = {'serial_number': None}

        # Get the Device ID for TEST-Router2
        res = self.client.get('/api/devices?name=TEST-Router2')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,400)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Updates from device require credentials.')

    @patch('application.get_serial_from_device')
    def test_api_update_serial_from_cisco_ios_bad_creds(self, mock_get_serial):
        """
        Test api update serial number from a Cisco IOS without credentials
        """

        update = {'serial_number': None, 'device_username': 'username',
            'device_password': 'bad password'}

        # get_serial_from_device returns None with bad credentials
        mock_get_serial.return_value = None

        # Get the Device ID for TEST-Router2
        res = self.client.get('/api/devices?name=TEST-Router2')
        id = res.get_json()['devices'][0]['id']

        # Send update request
        res = self.client.put(f'/api/devices/{id}', json=update)
        self.assertEqual(res.status_code,404)
        json_data = res.get_json()
        self.assertEqual(json_data['error'],'Unable to retrieve serial_number from device.')

    # Connectors tests - tests functions that collect information from
    # network devices.
    @patch('connectors.requests.get')
    def test_connectors_cisco_asa_get_version(self, mock_get):
        """ Test CiscoASA get version """

        mock_asa_resp = self.load_json_fixture('asa_api_get_version.json')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_asa_resp

        device = self.db.get_device_name('TEST-firewall1')
        res = get_version_from_device(device, 'username', 'password')
        self.assertEqual(res,mock_asa_resp['asaVersion'])

    @patch('connectors.requests.get')
    def test_connectors_cisco_asa_get_serial(self, mock_get):
        """ Test CiscoASA get serial  """

        mock_asa_resp = self.load_json_fixture('asa_get_serial.json')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_asa_resp

        device = self.db.get_device_name('TEST-firewall1')
        res = get_serial_from_device(device, 'username', 'password')
        self.assertEqual(res,mock_asa_resp['serialNumber'])

    @patch('connectors.requests.get')
    def test_connectors_cisco_asa_get_version_bad_creds(self, mock_get):
        """ Test Cisco ASA Get version with bad device credentials """

        # ASA API returns status code 401 when authentication fails
        mock_get.return_value.status_code = 401

        device = self.db.get_device_name('TEST-firewall1')
        res = get_version_from_device(device, 'username', 'badpass')
        self.assertEqual(res,None)

    @patch('connectors.requests.get')
    def test_connectors_cisco_asa_get_serial_bad_creds(self, mock_get):
        """ Test Cisco ASA Get serial with bad device credentials """

        # ASA API returns status code 401 when authentication fails
        mock_get.return_value.status_code = 401

        device = self.db.get_device_name('TEST-firewall1')
        res = get_serial_from_device(device, 'username', 'badpass')
        self.assertEqual(res,None)

    @patch('connectors.netmiko.ConnectHandler')
    def test_connectors_cisco_ios_get_version(self, mock_connect):
        """ Test CiscoIOS get version """

        mock_output = self.load_text_fixture('ios_show_version.txt')
        # Double return_value to mock the instance returned by ConnectHandler
        mock_connect.return_value.send_command.return_value = mock_output

        device = self.db.get_device_name('TEST-Router2')
        res = get_version_from_device(device, 'username', 'password')
        self.assertEqual(res,'12.4(24)T6')

    @patch('connectors.netmiko.ConnectHandler')
    def test_connectors_cisco_ios_get_serial(self, mock_connect):
        """ Test CiscoIOS get serial  """

        mock_output = self.load_text_fixture('ios_show_version.txt')
        # Double return_value to mock the instance returned by ConnectHandler
        mock_connect.return_value.send_command.return_value = mock_output

        device = self.db.get_device_name('TEST-Router2')
        res = get_serial_from_device(device, 'username', 'password')
        self.assertEqual(res,'4279256517')

    @patch('connectors.netmiko.ConnectHandler')
    def test_connectors_cisco_ios_get_version_bad_creds(self, mock_connect):
        """ Test Cisco IOS get version with bad device credentials """

        mock_connect.side_effect = netmiko.ssh_exception.NetMikoAuthenticationException
        device = self.db.get_device_name('TEST-Router2')
        res = get_version_from_device(device, 'username', 'badpass')
        self.assertEqual(res,None)

    @patch('connectors.netmiko.ConnectHandler')
    def test_connectors_cisco_ios_get_serial_bad_creds(self, mock_connect):
        """ Test Cisco IOS get serial with bad device credentials """

        mock_connect.side_effect = netmiko.ssh_exception.NetMikoAuthenticationException
        device = self.db.get_device_name('TEST-Router2')
        res = get_serial_from_device(device, 'username', 'badpass')
        self.assertEqual(res,None)


if __name__ == "__main__":
    unittest.main()
