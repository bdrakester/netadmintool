#!/usr/local/bin/python3

from flask import Flask, jsonify, request, url_for
from database import NetAdminToolDB
from connectors import get_version_from_device, get_serial_from_device

CONFIG_FILE = 'netadminapi.conf'
TESTING_CONFIG_FILE = 'tests.conf'

app = Flask(__name__)
app.config['DATABASE'] = NetAdminToolDB(CONFIG_FILE)

@app.route("/api")
def index():
    return jsonify({'Version':'Net Admin Tool v1.0'})

@app.route("/api/devices", methods=['GET'])
def get_devices():
    """
    Return all devices.
    Supported query strings:
        name: returns all devices with that name
    """
    name = request.args.get('name')
    netAdminToolDB = app.config['DATABASE']
    #print(f'DEBUG application.py get_devices() - db = {netAdminToolDB.dbname}')
    devices = netAdminToolDB.get_device()

    deviceList = []
    if name != None:
        for device in devices:
            if device.name == name:
                uri = url_for('get_device',device_id=device.id,_external=True)
                deviceList.append({
                                    'id': device.id,
                                    'uri': uri,
                                    'name': device.name,
                                    'ip_addr': device.ip_addr,
                                    'device_type_id': device.device_type_id,
                                    'make': device.make,
                                    'model': device.model,
                                    'code': device.code,
                                    'sw_version': device.sw_version,
                                    'serial_number': device.serial_number,
                                    'datacenter': device.datacenter,
                                    'location': device.location,
                                    'console': device.console,
                                    'description': device.description,
                                    'notes': device.notes
                                })
    else:
        for device in devices:
            uri = url_for('get_device',device_id=device.id,_external=True)
            deviceList.append({
                                'id': device.id,
                                'uri': uri,
                                'name': device.name,
                                'ip_addr': device.ip_addr,
                                'device_type_id': device.device_type_id,
                                'make': device.make,
                                'model': device.model,
                                'code': device.code,
                                'sw_version': device.sw_version,
                                'serial_number': device.serial_number,
                                'datacenter': device.datacenter,
                                'location': device.location,
                                'console': device.console,
                                'description': device.description,
                                'notes': device.notes
                            })

    if deviceList == []:
        return jsonify({'error': 'No devices found'}), 404

    return jsonify({'devices': deviceList})

@app.route("/api/devices/<int:device_id>", methods=['GET'])
def get_device(device_id):
    """
    Return device with id device_id
    """
    netAdminToolDB = app.config['DATABASE']
    device = netAdminToolDB.get_device(device_id)

    if device == None:
        return jsonify({'error': 'Device_id not found'}), 404

    uri = url_for('get_device',device_id=device.id,_external=True)
    return jsonify({'device':{
                                'id': device.id,
                                'uri': uri,
                                'name': device.name,
                                'ip_addr': device.ip_addr,
                                'device_type_id': device.device_type_id,
                                'make': device.make,
                                'model': device.model,
                                'code': device.code,
                                'sw_version': device.sw_version,
                                'serial_number': device.serial_number,
                                'datacenter': device.datacenter,
                                'location': device.location,
                                'console': device.console,
                                'description': device.description,
                                'notes': device.notes
                            }
                    })

@app.route("/api/devices/<int:device_id>", methods=['PUT'])
def update_device(device_id):
    """
    Update device with id device_id.
    If JSON value = None for a supported key, connect to device to retrieve
    updated value. Also requires keys device_username and device_password
    Supported keys for device update: sw_version, serial_number
    """
    netAdminToolDB = app.config['DATABASE']
    device = netAdminToolDB.get_device(device_id)
    #print(f'update_device request = {request.get_data()}')
    if device == None:
        return jsonify({'error': 'Device_id not found'}), 404

    input = request.get_json()

    if input == None:
        return jsonify({'error': 'Invalid PUT request'}), 400

    # Get update values from device for supported keys with value None
    if 'sw_version' in input and input['sw_version'] == None:
        # If device credentials were provided
        if 'device_username' and 'device_password' in input:
            input['sw_version'] = get_version_from_device(device,
                input['device_username'], input['device_password'])
            if input['sw_version'] == None:
                return jsonify({'error': 'Unable to retrieve sw_version from device.'}), 404
        # Device credentials not provided, return error
        else:
            return jsonify({'error': 'Updates from device require credentials.'}), 400

    if 'serial_number' in input and input['serial_number'] == None:
        # If device credentials were provided
        if 'device_username' and 'device_password' in input:
            input['serial_number'] = get_serial_from_device(device,
                input['device_username'], input['device_password'])
            if input['serial_number'] == None:
                return jsonify({'error': 'Unable to retrieve serial_number from device.'}), 404
        # Device credentials not provided, return error
        else:
            return jsonify({'error': 'Updates from device require credentials.'}), 400

    # Send input directly to update_device function, which checks each key.
    netAdminToolDB.update_device(device_id, **input)
    device = netAdminToolDB.get_device(device_id)
    deviceDict = dict(device)
    uri = url_for('get_device',device_id=device.id,_external=True)
    deviceDict['uri'] = uri

    return jsonify({'device': deviceDict}), 200


@app.route("/api/devices", methods=['POST'])
def add_device():
    """
    Add a new device
    """
    input = request.get_json()

    if input == None:
        return jsonify({'error': 'Invalid POST request, no data'}), 400
    if not 'name' in input:
        return jsonify({'error': 'Invalid POST request, missing name'}), 400
    if not 'ip_addr' in input:
        return jsonify({'error': 'Invalid POST request, missing ip_addr'}), 400
    if not 'device_type_id' in input:
        return jsonify({'error': 'Invalid POST request, missing device_type_id'}), 400
    if not 'sw_version' in input:
        return jsonify({'error': 'Invalid POST request, missing sw_version'}), 400
    if not 'serial_number' in input:
        return jsonify({'error': 'Invalid POST request, missing serial_number'}), 400
    if not 'datacenter' in input:
        return jsonify({'error': 'Invalid POST request, missing datacenter'}), 400
    if not 'location' in input:
        return jsonify({'error': 'Invalid POST request, missing location'}), 400

    if not 'console' in input:
        input['console'] = ''
    if not 'description' in input:
        input['description'] = ''
    if not 'notes' in input:
        input['notes'] = ''

    netAdminToolDB = app.config['DATABASE']
    id = netAdminToolDB.add_device(input['name'], input['ip_addr'],
        input['device_type_id'], input['sw_version'],
        input['serial_number'], input['datacenter'], input['location'],
        input['console'], input['description'], input['notes'])

    device = netAdminToolDB.get_device(id)
    deviceDict = dict(device)
    uri = url_for('get_device',device_id=device.id,_external=True)
    deviceDict['uri'] = uri

    return jsonify({'device':deviceDict}), 201

@app.route("/api/devices/<int:device_id>", methods=['DELETE'])
def delete_device(device_id):
    """
    Delete device with device_id
    """
    netAdminToolDB = app.config['DATABASE']
    device = netAdminToolDB.get_device(device_id)

    if device == None:
        return jsonify({'error': 'Device_id not found'}), 404

    netAdminToolDB.delete_device(device_id)
    return jsonify({'result': True})

@app.route("/api/users", methods=['GET'])
def get_users():
    """
    Return all users. Does not return password
    Supported query strings:
        username: returns user with supplied name
    """
    username = request.args.get('username')
    netAdminToolDB = app.config['DATABASE']
    if username != None:
        users = []
        users.append(netAdminToolDB.get_user_name(username))
    else:
        users = netAdminToolDB.get_user()

    userList = []
    for user in users:
        uri = url_for('get_user', user_id=user.id,_external=True)
        #role = netAdminToolDB.get_role(user.role_id)
        userList.append({
                        'id': user.id,
                        'uri': uri,
                        'username': user.username,
                        'display_name': user.display_name,
                        'role': user.role_name
                        })
    if userList == []:
        return jsonify({'error': 'No users found'}), 404

    return jsonify({'users': userList })

@app.route("/api/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    """
    Return user with id user_id
    """
    netAdminToolDB = app.config['DATABASE']
    user = netAdminToolDB.get_user(user_id)

    if user == None:
        return jsonify({'error': 'User_id not found'}), 404

    uri = url_for('get_user', user_id=user.id, _external=True)
    return jsonify({'user':{
                            'id': user.id,
                            'uri': uri,
                            'username': user.username,
                            'display_name': user.display_name,
                            'role': user.role_name
                            }
                    })

@app.route("/api/users/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    """
    Update user with user_id
    """
    netAdminToolDB = app.config['DATABASE']
    user = netAdminToolDB.get_user(user_id)
    if user == None:
        return jsonify({'error': 'User_id not found'}), 404

    input = request.get_json()

    if input == None:
        return jsonfiy({'error': 'Invalid PUT request'}), 400

    # Send input directly to update_user function, which checks each key
    netAdminToolDB.update_user(user_id, **input)
    user = netAdminToolDB.get_user(user_id)
    userDict = dict(user)
    uri = url_for('get_user', user_id=user.id, _external=True)
    userDict['uri'] = uri

    return jsonify({'user': userDict}), 200


@app.route("/api/users", methods=['POST'])
def add_user():
    """
    Add a new user
    """
    input = request.get_json()

    if input == None:
        return jsonify({'error': 'Invalid POST request, no data'}), 400
    if not 'username' in input:
        return jsonify({'error': 'Invalid POST request, missing username'}), 400
    if not 'password' in input:
        return jsonify({'error': 'Invalid POST request, missing password'}), 400
    if not 'display_name' in input:
        return jsonify({'error': 'Invalid POST request, missing display_name'}), 400
    if not 'role' in input:
        return jsonify({'error': 'Invalid POST request, missing role'}), 400

    netAdminToolDB = app.config['DATABASE']
    id = netAdminToolDB.add_user(input['username'], input['password'],
        input['display_name'], input['role'])

    newUser = netAdminToolDB.get_user(id)
    newUserDict = dict(newUser)
    uri = url_for('get_user', user_id=newUser.id, _external=True)
    newUserDict['uri'] = uri

    return jsonify({'user': newUserDict}), 201

@app.route("/api/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    """
    Delete user with user_id
    """
    netAdminToolDB = app.config['DATABASE']
    user = netAdminToolDB.get_user(user_id)

    if user == None:
        return jsonify({'error': 'User_id not found'}), 404

    netAdminToolDB.delete_user(user_id)
    return jsonify({'result': True})

@app.route("/api/users/validate", methods=['PUT'])
def validate_user():
    netAdminToolDB = app.config['DATABASE']
    input = request.get_json()

    if input == None:
        return jsonify({'error': 'Invalid PUT request, no data'}), 400
    if not 'username' in input:
        return jsonify({'error': 'Invalid PUT request, missing username'}), 400
    if not 'password' in input:
        return jsonify({'error': 'Invalid PUT request, missing password'}), 400

    if netAdminToolDB.authenticate_user(input['username'], input['password']):
        return jsonify({'result': True})

    return jsonify({'result': False}), 404

@app.route('/api/device_types', methods=['GET'])
def get_device_types():
    """
    Return all device types.
    """
    netAdminToolDB = app.config['DATABASE']

    device_types = netAdminToolDB.get_device_type()
    list = []
    for device_type in device_types:
        uri = url_for('get_device_type', device_type_id=device_type.id, _external=True)
        list.append({
                    'id': device_type.id,
                    'uri': uri,
                    'make': device_type.make,
                    'model': device_type.model,
                    'code': device_type.code
                    })
    if list == []:
        return jsonify({'error': 'No device types found'}), 404

    return jsonify({'device_types': list})

@app.route('/api/device_types/<int:device_type_id>', methods=['GET'])
def get_device_type(device_type_id):
    """
    Return device_type with device_type_id.
    """
    netAdminToolDB = app.config['DATABASE']
    device_type = netAdminToolDB.get_device_type(device_type_id)

    if device_type == None:
        return jsonify({'error': 'device_type_id not found'}), 404

    return jsonify({'device_type':  {
                                    'id': device_type.id,
                                    'make': device_type.make,
                                    'model': device_type.model,
                                    'code': device_type.code
                                    }


                })

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def bad_request(error):
    return jsonify({'error': 'Not found'}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
