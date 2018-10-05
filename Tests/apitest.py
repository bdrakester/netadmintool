import requests

def print_response(response):
    print('\nResponse Headers: \n')
    print(response.headers)
    print('\nResponse Content: \n')
    print(response.text)

def main():
    print('Testing Net Admin Tool API\n')
    print('Get all devices ...')
    print('GET /api/devices')

    resp = requests.get('http://127.0.0.1:5000/api/devices')
    print_response(resp)

    print('')

if __name__ == '__main__':
    main()
