from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/devices/<int:device_id>', methods=['GET'])
def device(device_id):
    resp = requests.get(f'{api}/devices/{device_id}')
    if resp.status_code == 200:
        device = resp.json()['device']
        return render_template('device.html', device = device)
    else:
        return render_template('error.html', message = "Device not found.")

@app.route('/devices/<int:device_id>', methods=['POST'])
def update_device(device_id):
    attribute = request.form.get('attribute')
    new_value = request.form.get('new_value')

    # If new value entered in form, call api to update database
    if new_value != '':
        update = {attribute:new_value}
        resp = requests.put(f'{api}/devices/{device_id}', json=update)

    return redirect(url_for('device', device_id = device_id))


@app.route('/devices/delete/<int:device_id>')
def delete_device(device_id):
    error = "An error occured, the device was not deleted."
    success = "Device deleted."

    resp = requests.delete(f'{api}/devices/{device_id}')

    if resp.status_code != 200:
        return render_template('delete.html', message = error)

    return render_template('delete.html', message = success)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
