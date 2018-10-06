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
    postData = {'name': newName, 'device_type':'test_type',
                'description':f'Desc of {newName}'}
    print(f'POST Data = {postData}')
    print(f'POST {hostname}:5000/api/devices')
    resp = requests.post(f'http://{hostname}:5000/api/devices',json=postData)
    print_response(resp)
    addedDevice = resp.json()
    newID = addedDevice['success']['id']

    print(f'Updating Device {newID} ...')
    putData = {'description':f'PUT Updated Desc of {newID}'}
    print(f'PUT data = {putData}')
    print(f'PUT {hostname}:5000/api/devices/{newID}')
    resp = requests.put(f'http://{hostname}:5000/api/devices/{newID}',json=putData)
    print_response(resp)

    print(f'Deleting Device {newID} ...')
    url = f'http://{hostname}:5000/api/devices/{newID}'
    print(f'DELETE {url}')
    resp = requests.delete(url)
    print_response(resp)

    print(f'Get device{newID} ...')
    url = f'http://{hostname}:5000/api/devices/{newID}'
    resp = requests.get(url)
    print_response(resp)

if __name__ == '__main__':
    main()
