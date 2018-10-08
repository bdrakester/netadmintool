#!/usr/local/bin/python3

from flask import Flask, jsonify, request, url_for
from database import NetAdminToolDB

app = Flask(__name__)
netAdminToolDB = NetAdminToolDB("netadminapi.conf")

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

    devices = netAdminToolDB.get_device()
    deviceList = []
    if name != None:
        for device in devices:
            if device.name == name:
                uri = url_for('get_device',device_id=device.id,_external=True)
                deviceList.append({
                                    'uri': uri,
                                    'name': device.name,
                                    'device_type': device.device_type,
                                    'description': device.description
                                })
    else:
        for device in devices:
            uri = url_for('get_device',device_id=device.id,_external=True)
            deviceList.append({
                            'uri': uri,
                            'name': device.name,
                            'device_type': device.device_type,
                            'description': device.description
                            })

    if deviceList == []:
        return jsonify({'error': 'No devices found'}), 404

    return jsonify({'devices': deviceList})

@app.route("/api/devices/<int:device_id>", methods=['GET'])
def get_device(device_id):
    """
    Return device with id device_id
    """
    device = netAdminToolDB.get_device(device_id)

    if device == None:
        return jsonify({'error': 'Device_id not found'}), 404

    uri = url_for('get_device',device_id=device.id,_external=True)
    return jsonify({'device':{
                                'uri': uri,
                                'name': device.name,
                                'device_type': device.device_type,
                                'description': device.description
                            }
                    })

@app.route("/api/devices/<int:device_id>", methods=['PUT'])
def update_device(device_id):
    """
    Update device with id device_id
    """
    device = netAdminToolDB.get_device(device_id)
    if device == None:
        return jsonify({'error': 'Device_id not found'}), 404

    input = request.get_json()

    if input == None:
        return jsonify({'error': 'Invalid PUT request'}), 400

    updates = dict()
    updates['name'] = input.get('name',device.name)
    updates['device_type'] = input.get('device_type',device.device_type)
    updates['description'] = input.get('description', device.description)

    netAdminToolDB.update_device(device_id, updates)
    device = netAdminToolDB.get_device(device_id)
    deviceDict = dict(device)
    uri = url_for('get_device',device_id=device.id,_external=True)
    deviceDict['uri'] = uri
    del deviceDict['id']
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
    if not 'device_type' in input:
        return jsonify({'error': 'Invalid POST request, missing device_type'}), 400

    if not 'description' in input:
        id = netAdminToolDB.add_device(input['name'],input['device_type'])
        device = netAdminToolDB.get_device(id)
        return jsonify({'success':dict(device)}), 201

    id = netAdminToolDB.add_device(input['name'],input['device_type'],
                            input['description'])
    device = netAdminToolDB.get_device(id)
    deviceDict = dict(device)
    uri = url_for('get_device',device_id=device.id,_external=True)
    deviceDict['uri'] = uri
    del deviceDict['id']
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
