from os import path
from base64 import b64decode
from json import load

_basedir = path.abspath(path.dirname(__file__))

_config_path = path.join(_basedir, '..', '..', 'alicehm-cfg', 'config.json')


def _get_config():
    with open(_config_path, 'r') as f:
        return load(f)


config = _get_config()

DATA_BASE_CONNECTION_STRING = config['DATA_BASE_CONNECTION_STRING']
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']
LOGIN = config['LOGIN']
PASSWORD = config['PASSWORD']
DEVICE_CTRL_SERVER_URL = config['DEVICE_CTRL_SERVER_URL']
DEVICES = config['DEVICES']
