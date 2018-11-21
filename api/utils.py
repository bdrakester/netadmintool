#!/usr/local/bin/python3
#####################################################################
# utils.py
#
# Provides functions to collect information from network devices.
#####################################################################

import urllib3
import requests
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()

def get_version_from_device(device):
    """ Retrieves the sw_version  from device """
    if device.model.startswith('ASA'):
        return CiscoASA.get_version(device.ip_addr)

    return None

class CiscoASA:

    @staticmethod
    def get_version(hostname):
        server = hostname
        api_path = 'api/monitoring/device/components/version'
        resp = requests.get(f'https://{server}/{api_path}',auth=HTTPBasicAuth('',''),
            verify=False)
        version = resp.json()['asaVersion']
        return version



if __name__ == '__main__':
    server = '10.20.1.2'
    api = 'api/monitoring/device/components/version'

    resp = requests.get(f'https://{server}/{api}',auth=HTTPBasicAuth('',''),
        verify=False)

    print(f'status_code = {resp.status_code}')
    print(f'text = {resp.text}')
