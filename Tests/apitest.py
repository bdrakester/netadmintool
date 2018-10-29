import requests, sys

def print_response(response):
    print(f'Response code: {response.status_code}\n')
    print('Response Headers: \n')
    print(response.headers)
    print('\nResponse Content: \n')
    print(response.text)

def main():
    hostname = sys.argv[1]
    device = sys.argv[2]
    newName = sys.argv[3]

    print('Testing Net Admin Tool API\n')

    print('Get all devices ...')
    print(f'GET {hostname}:5000/api/devices')

    resp = requests.get(f'http://{hostname}:5000/api/devices')
    print_response(resp)

    print(f'Getting Device {device} ...')
    print(f'GET {hostname}:5000/api/devices/{device}')

    resp = requests.get(f'http://{hostname}:5000/api/devices/{device}')
    print_response(resp)

    print(f'Adding Device {newName} ... ')
    postData = {'name': newName, 'ip_addr': '192.168.1.2',
        'device_type':'test_type', 'make':'test make', 'model':'test model',
        'sw_version': '1337', 'serial_number':'snTEST', 'datacenter':'Test DC',
        'location': 'Test Location', 'console': 'Test 1',
        'description':f'Desc of {newName}', 'notes':f'Notes re:{newName}'}

    print(f'POST Data = {postData}')
    print(f'POST {hostname}:5000/api/devices')
    resp = requests.post(f'http://{hostname}:5000/api/devices',json=postData)
    print_response(resp)
    addedDevice = resp.json()
    #newID = addedDevice['success']['id']
    newURI = addedDevice['device']['uri']

    print(f'Updating Device {newURI} ...')
    putData = {'description':f'PUT Updated Desc of {newURI}'}
    print(f'PUT data = {putData}')
    print(f'PUT {newURI}')
    resp = requests.put(f'{newURI}',json=putData)
    print_response(resp)

    print(f'Deleting Device {newURI} ...')
    #url = f'http://{hostname}:5000/api/devices/{newID}'
    print(f'DELETE {newURI}')
    resp = requests.delete(newURI)
    print_response(resp)

    print(f'Get device {newURI} ...')
    #url = f'http://{hostname}:5000/api/devices/{newID}'
    resp = requests.get(newURI)
    print_response(resp)

if __name__ == '__main__':
    main()
