from flask import Flask, render_template
import requests
from configparser import ConfigParser

CONFIGFILE = 'netadminapp.conf'

app = Flask(__name__)

config = ConfigParser()
config.read(CONFIGFILE)
hostname = config['API']['hostname']
port = config['API']['port']

@app.route('/')
def index():
    resp = requests.get(f'http://{hostname}:{port}/api/devices')
    devices = resp.json()
    return render_template('index.html', devices = devices['devices'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
