import requests

from alice_app import config


class DeviceClient:
    @staticmethod
    def get_device(device_name: str) -> dict:
        url = f'{config.DEVICE_CTRL_SERVER_URL}/get-mqtt-device'
        data = {"device_name": device_name}
        response = requests.post(url, data)
        return response.json()

    @staticmethod
    def set_switch_state(device_name: str, new_state: bool):
        url = f'{config.DEVICE_CTRL_SERVER_URL}/turn-mqtt-switch'
        data = {
            "device_name": device_name,
            "new_state": new_state
        }
        requests.post(url, data)

    @staticmethod
    def set_motor(device_name: str, position: int):
        url = f'{config.DEVICE_CTRL_SERVER_URL}/set-mqtt-motor'
        data = {
            "device_name": device_name,
            "position": position
        }
        requests.post(url, data)
