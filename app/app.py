from flask import Flask, render_template
import requests
from configparser import ConfigParser

CONFIGFILE = 'netadminapp.conf'

app = Flask(__name__)

config = ConfigParser()
config.read(CONFIGFILE)
hostname = config['API']['hostname']
port = config['API']['port']
api = f'http://{hostname}:{port}/api'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
def devices():
    resp = requests.get(f'{api}/devices')
    devices = resp.json()['devices']
    return render_template('devices.html', devices = devices)

@app.route('/devices/<int:device_id>')
def device(device_id):
    resp = requests.get(f'{api}/devices/{device_id}')
    if resp.status_code == 200:
        device = resp.json()['device']
        return render_template('device.html', device = device)
    else:
        return render_template('error.html', message = "Device not found.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
