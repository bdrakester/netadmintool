#!/usr/local/bin/python3

from flask import Flask, jsonify, request, url_for, g
from database import NetAdminToolDB

CONFIG_FILE = 'netadminapi.conf'
TESTING_CONFIG_FILE = 'tests.conf'

app = Flask(__name__)
app.config['DATABASE'] = NetAdminToolDB(CONFIG_FILE)
netAdminToolDB = NetAdminToolDB('netadminapi.conf')
#print('DEBUG: application.py - just created netAdminToolDB from netadminapi.conf')

@app.route("/api")
def index():
    return jsonify({'Version':'Net Admin Tool v1.0'})

@app.route("/api/devices", methods=['GET'])
def get_devices():
    """
    Return all devices. Support query strings: name.
    Name: returns all devices with that name
    """
    name = request.args.get('name')
    netAdminToolDB = app.config['DATABASE']
    #print(f'DEBUG application.py get_devices() - db = {db.dbname}')
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
                                    'device_type': device.device_type,
                                    'make': device.make,
                                    'model': device.model,
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
                                'device_type': device.device_type,
                                'make': device.make,
                                'model': device.model,
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
                                'device_type': device.device_type,
                                'make': device.make,
                                'model': device.model,
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
    Update device with id device_id
    """
    netAdminToolDB = app.config['DATABASE']
    device = netAdminToolDB.get_device(device_id)
    if device == None:
        return jsonify({'error': 'Device_id not found'}), 404

    input = request.get_json()

    if input == None:
        return jsonify({'error': 'Invalid PUT request'}), 400

    # Send input directly to update_device function, which checks each key.
    netAdminToolDB.update_device(device_id, **input)
    device = netAdminToolDB.get_device(device_id)
    deviceDict = dict(device)
    uri = url_for('get_device',device_id=device.id,_external=True)
    deviceDict['uri'] = uri
    #del deviceDict['id']
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
    if not 'device_type' in input:
        return jsonify({'error': 'Invalid POST request, missing device_type'}), 400
    if not 'make' in input:
        return jsonify({'error': 'Invalid POST request, missing make'}), 400
    if not 'model' in input:
        return jsonify({'error': 'Invalid POST request, missing model'}), 400
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

    id = netAdminToolDB.add_device(input['name'], input['ip_addr'],
        input['device_type'], input['make'], input['model'],
        input['sw_version'], input['serial_number'], input['datacenter'],
        input['location'], input['console'], input['description'],
        input['notes'])

    device = netAdminToolDB.get_device(id)
    deviceDict = dict(device)
    uri = url_for('get_device',device_id=device.id,_external=True)
    deviceDict['uri'] = uri

    return jsonify({'device':deviceDict}), 201

@app.route("/api/devices/<int:device_id>", methods=['DELETE'])
def delete_device(device_id):
    device = netAdminToolDB.get_device(device_id)

    if device == None:
        return jsonify({'error': 'Device_id not found'}), 404

    netAdminToolDB.delete_device(device_id)
    return jsonify({'result': True})

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def bad_request(error):
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':

    app.run(host='0.0.0.0',debug=True)
