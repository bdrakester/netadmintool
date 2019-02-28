#!/usr/local/bin/python3
#####################################################################
# connectors.py
#
# Provides functions to collect information from network devices.
#####################################################################

import urllib3
import netmiko
import re
import requests
from requests.auth import HTTPBasicAuth

#remove import sys later, used to print exceptions, remove print statements too
#import sys

requests.urllib3.disable_warnings()

def get_version_from_device(device, username, password):
    """
    Retrieves the software version (sw_version) from device, returns None
    there as an error.
    """
    if device.code == 'cisco_asa':
        return CiscoASA.get_version(device.ip_addr, username, password)

    if device.code == 'cisco_ios':
        return CiscoIOS.get_version(device.ip_addr, username, password)

    return None

def get_serial_from_device(device, username, password):
    """
    Retrieves the serial number from device, returns None if there was
    an error.
    """
    if device.code == 'cisco_asa':
        return CiscoASA.get_serial(device.ip_addr, username, password)

    if device.code == 'cisco_ios':
        return CiscoIOS.get_serial(device.ip_addr, username, password)

    return None

class CiscoASA:

    @staticmethod
    def get_version(hostname, username, password):
        """ Retrieve software version from device, returns None if error """
        server = hostname
        api_path = 'api/monitoring/device/components/version'
        resp = requests.get(f'https://{server}/{api_path}',
            auth=HTTPBasicAuth(username,password), verify=False)

        if resp.status_code == 200:
            return resp.json()['asaVersion']

        return None

    @staticmethod
    def get_serial(hostname, username, password):
        """
        Retrieve serial number from device, returns None if error.
        """
        server = hostname
        api_path = 'api/monitoring/serialnumber'
        resp = requests.get(f'https://{server}/{api_path}',
            auth=HTTPBasicAuth(username,password), verify=False)

        if resp.status_code == 200:
            return resp.json()['serialNumber']

        return None

class CiscoIOS:
    @staticmethod
    def get_version(hostname, username, password):
        """
        Retrieve software version from Cisco IOS device, returns None if error.
        """
        device = {
            'ip': hostname,
            'device_type': 'cisco_ios',
            'username': username,
            'password': password
        }
        try:
            connection = netmiko.ConnectHandler(**device)
            output = connection.send_command('show version')
            #match = re.search(r'Version (\d+\.\d+\(\d+\)\w+)', output)
            # When testing on 7200 - version number had number and character
            # in between () and nothing after ()
            match = re.search(r'Version (\d+\.\d+\(\w+\)\w*)', output)
            connection.disconnect()
            return match.group(1)
        except:
            #e = sys.exc_info()[0]
            #print(f'\nIOS get_version except - e = {e}')
            return None

    @staticmethod
    def get_serial(hostname, username, password):
        """
        Retrieve serial number from Cisco IOS device, returns None if error.
        """
        device = {
            'ip': hostname,
            'device_type': 'cisco_ios',
            'username': username,
            'password': password
        }
        try:
            connection = netmiko.ConnectHandler(**device)
            output = connection.send_command('show version')
            match = re.search(r'Processor board ID (\w+)', output)
            connection.disconnect()
            return match.group(1)
        except:
            #e = sys.exc_info()[0]
            #print(f'\nIOS get_serial except - e = {e}')
            return None


if __name__ == '__main__':
    """
    # For Testing ASA
    server = '10.20.1.2'
    api = 'api/monitoring/device/components/version'

    resp = requests.get(f'https://{server}/{api}',auth=HTTPBasicAuth('',''),
        verify=False)

    print(f'status_code = {resp.status_code}')
    print(f'text = {resp.text}')
    """

    #For Testing CiscoIOS
