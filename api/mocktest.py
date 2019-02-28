# mocktest.py
# Testing unittest.mock before adding to test.py

import os
import json
import unittest
from unittest.mock import Mock, patch
from configparser import ConfigParser

from database import NetAdminToolDB as DB
from application import app
from connectors import get_version_from_device, get_serial_from_device, requests

# Contains test database connection information
CONFIG_FILE = 'tests.conf'

FIXTURE_PATH = os.path.join('.', 'fixtures')

class Mocktest(unittest.TestCase):
    @classmethod
    def setUpClass(self):

        requests.urllib3.disable_warnings()
        self.db = DB(CONFIG_FILE)
        config = ConfigParser()
        config.read(CONFIG_FILE)

        # Import credentials and ip addresses for connectors tests
        # For future, should mock this api
        self.ios_ip = config['IOS']['ip']
        self.ios_username = config['IOS']['username']
        self.ios_password = config['IOS']['password']
        self.ios_version = config['IOS']['version']
        self.ios_serial = config['IOS']['serial']


    def setUp(self):
        self.db.create_tables()
        self.db.add_device('TEST-firewall1', '1.1.1.1', 1,
            '9.7', 'sn7890', 'Boston', 'Rack 1', 'Serial 2',
            'NGFW', 'Notes for firewall1')
        self.db.add_device('TEST-switch1', '3.3.3.3', 3,
            '3.1.4', 'sn9876', 'Boston', 'Rack 2', 'Serial 3', 'Core switch',
            'Notes for switch1')
        self.db.add_device('TEST-Router2', self.ios_ip, 2,
            '12.1', 'sn456', 'Boston', 'Rack 2', 'Serial 4', 'Core Router',
            'Notes for Router2')

        self.db.add_user('TestAdmin','password','TestAdmin Display','admin')

        app.config['DATABASE'] = DB(CONFIG_FILE)
        self.client = app.test_client()
        self.client.testing = True

    def load_json_fixture(self, name):
        file = os.path.join(FIXTURE_PATH,name)
        with open(file) as fixture_file:
            data = json.load(fixture_file)

        return data

    def load_text_fixture(self, name):
        file = os.path.join(FIXTURE_PATH,name)
        with open(file) as fixture_file:
            data = fixture_file.read()

        return data

    @unittest.skip("Skip")
    @patch('connectors.requests.get')
    def test_connectors_cisco_asa_get_version(self, mock_get):
        """ Test CiscoASA get version """

        mock_api_resp = self.load_json_fixture('asa_api_get_version.json')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_api_resp

        device = self.db.get_device_name('TEST-firewall1')
        res = get_version_from_device(device, self.asa_username,
            self.asa_password)
        self.assertEqual(res,mock_api_resp['asaVersion'])

    @unittest.skip("Skip")
    @patch('connectors.requests.get')
    def test_connectors_cisco_asa_get_serial(self, mock_get):
        """ Test CiscoASA get serial  """

        mock_api_resp = self.load_json_fixture('asa_get_serial.json')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_api_resp

        device = self.db.get_device_name('TEST-firewall1')
        res = get_serial_from_device(device, self.asa_username,
            self.asa_password)
        self.assertEqual(res,mock_api_resp['serialNumber'])

    @unittest.skip("Skip")
    @patch('application.get_version_from_device')
    def test_api_update_version_from_cisco_asa(self, mock_get_version):

        mock_get_version.return_value = '9.8(1)'

        """ Test api update software version from a Cisco ASA """
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

    @patch('connectors.netmiko.ConnectHandler')
    def test_connectors_cisco_ios_get_version(self, mock_connect):
        """ Test CiscoIOS get version """

        mock_output = self.load_text_fixture('ios_show_version.txt')
        # Double return_value to mock the instance returned by ConnectHandler
        mock_connect.return_value.send_command.return_value = mock_output

        device = self.db.get_device_name('TEST-Router2')
        res = get_version_from_device(device, self.ios_username,
            self.ios_password)
        self.assertEqual(res,'12.4(24)T6')

if __name__ == "__main__":
    unittest.main()
