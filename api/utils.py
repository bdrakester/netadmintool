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

def get_from_device(device, attribute):
    """ Retrieves attribute from device """
    if attribute == 'sw_version':
        if device.model.startswith('ASA'):
            return CiscoASA.get_version()

    return None

class CiscoASA:

    @staticmethod
    def get_version(device):
        api_path = 'api/monitoring/device/components/version'
        requests.get(f'https://{server}/{api}',auth=HTTPBasicAuth('',''),
            verify=False)
        return '9.2'


server = '172.26.13.18'
api = 'api/monitoring/device/components/version'

resp = requests.get(f'https://{server}/{api}',auth=HTTPBasicAuth('',''),
    verify=False)

print(f'status_code = {resp.status_code}')
print(f'text = {resp.text}')
