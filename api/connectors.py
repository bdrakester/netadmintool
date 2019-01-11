#!/usr/local/bin/python3
#####################################################################
# connectors.py
#
# Provides functions to collect information from network devices.
#####################################################################

import urllib3
import requests
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()

def get_version_from_device(device,username,password):
    """
    Retrieves the software version (sw_version) from device, returns None
    there as an error.
    """
    if device.code == 'cisco_asa':
        return CiscoASA.get_version(device.ip_addr,username,password)

    return None

def get_serial_from_device(device, username, password):
    """
    Retrieves the serial number from device, returns None if there was
    an error.
    """
    if device.code == 'cisco_asa':
        return CiscoASA.get_serial(device.ip_addr, username, password)

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
        """ Retrieve serial number from device, returns None if error """
        server = hostname
        api_path = 'api/monitoring/serialnumber'
        resp = requests.get(f'https://{server}/{api_path}',
            auth=HTTPBasicAuth(username,password), verify=False)

        if resp.status_code == 200:
            return resp.json()['serialNumber']

        return None


if __name__ == '__main__':
    server = '10.20.1.2'
    api = 'api/monitoring/device/components/version'

    resp = requests.get(f'https://{server}/{api}',auth=HTTPBasicAuth('',''),
        verify=False)

    print(f'status_code = {resp.status_code}')
    print(f'text = {resp.text}')
