from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from configparser import ConfigParser
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_login import logout_user

CONFIGFILE = 'netadminapp.conf'

app = Flask(__name__)

config = ConfigParser()
config.read(CONFIGFILE)
hostname = config['API']['hostname']
port = config['API']['port']
api = f'http://{hostname}:{port}/api'
secret_key = config['SECURITY']['secret_key']
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, attributes):
        self.id = attributes['id']
        self.username = attributes['username']
        self.display_name = attributes['display_name']
        self.role = attributes['role']


def authenticate_user(username, password):
    """ Returns True if credentials are valid """
    creds = {'username': username, 'password': password}
    resp = requests.put(f'{api}/users/validate', json=creds)
    result = resp.json()['result']
    return result

@login_manager.user_loader
def load_user(user_id):
    resp = requests.get(f'{api}/users/{user_id}')

    if resp.status_code == 404:
        return
    attributes = resp.json()['user']
    user = User(attributes)

    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('error.html', message='Login required')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices', methods=['GET'])
def devices():
    resp = requests.get(f'{api}/devices')
    if resp.status_code == 200:
        devices = resp.json()['devices']
        return render_template('devices.html', devices = devices)
    else:
        return render_template('devices.html')


@app.route('/devices/<int:device_id>', methods=['GET'])
def device(device_id):
    resp = requests.get(f'{api}/devices/{device_id}')
    if resp.status_code == 200:
        resp_types = requests.get(f'{api}/device_types')
        device_types = resp_types.json()['device_types']
        device_types_list = []
        for device_type in device_types:
            device_types_list.append({
                                    'id': device_type['id'],
                                    'make': device_type['make'],
                                    'model': device_type['model']
                                    })
        device = resp.json()['device']
        return render_template('device.html', device = device,
            device_types= device_types_list)
    else:
        return render_template('error.html', message = "Device not found.")

@app.route('/devices/<int:device_id>', methods=['POST'])
def update_device(device_id):
    """ Update a device attribute """
    attribute = request.form.get('attribute')
    new_value = request.form.get('new_value')

    # If new value entered in form, call api to update database
    if new_value != '':
        update = {attribute:new_value}
        resp = requests.put(f'{api}/devices/{device_id}', json=update)

    # Else new value left empty, call API with JSON value set to None
    # to update from the device
    else:
        if attribute == 'sw_version' or attribute == 'serial_number':
            device_username = request.form.get('device_username')
            device_password = request.form.get('device_password')
            update = {attribute: None, 'device_username': device_username,
                'device_password':device_password}
            resp = requests.put(f'{api}/devices/{device_id}', json=update)

    return redirect(url_for('device', device_id = device_id))


@app.route('/devices/delete/<int:device_id>')
def delete_device(device_id):
    error = "An error occured, the device was not deleted."
    success = "Device deleted."

    resp = requests.delete(f'{api}/devices/{device_id}')

    if resp.status_code != 200:
        return render_template('error.html', message = error)

    #return render_template('delete.html', message = success)
    return redirect((url_for('devices')))


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        new_device = dict()
        for attribute in request.form:
            new_device[attribute] = request.form.get(attribute)

        resp = requests.post(f'{api}/devices', json = new_device)
        if resp.status_code == 400:
            error = resp.json()['error']
            return render_template('add.html', message = error)

        if resp.status_code == 201:
            device = resp.json()['device']
            return redirect((url_for('devices', device_id = device['id'])))

    resp = requests.get(f'{api}/device_types')
    if resp.status_code == 200:
        device_types = resp.json()['device_types']

    return render_template('add.html', device_types = device_types)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if authenticate_user(username, password):
        resp = requests.get(f'{api}/users?username={username}')
        attributes = resp.json()['users'][0]
        user = User(attributes)

        login_user(user)
        return redirect(url_for('index'))

    url = url_for('error') + '?type=authn'
    return redirect(url)

@app.route('/error', methods=['GET'])
def error():
    error = request.args.get('type')
    if error == 'authn':
        message = 'Login failed.  Please check username or password and \
            try again.'
        return render_template('error.html', message=message)
    return render_template('error.html', message='An error occured')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
