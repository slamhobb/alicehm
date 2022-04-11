from typing import List

import inject

from alice_app import config
from alice_app.business.device_client import DeviceClient


class SmartHomeService:
    device_client = inject.attr(DeviceClient)

    def get_devices(self, request_id: str) -> dict:
        res = {
            "request_id": request_id,
            "payload": {
                "user_id": "1",
                "devices": [cfg_device['yandex_data'] for cfg_device in config.DEVICES]
            }
        }

        return res

    def query_devices(self, request_id: str, data: dict) -> dict:
        def get_device_data(request_device_id: str) -> dict:
            cfg_device = self._get_cfg_device_by_yandex_id(request_device_id)
            cfg_device_name = cfg_device['name']
            device_data = self.device_client.get_device(cfg_device_name)
            return dict(request_device_id=request_device_id, device_data=device_data)

        def map_capabilities(device_data: dict) -> List[dict]:
            capabilities = []
            for name, value in device_data.items():
                if name == 'state':
                    capabilities.append({
                        "type": "devices.capabilities.on_off",
                        "state": {
                            "instance": "on",
                            "value": value
                        }
                    })
            return capabilities

        def map_properties(device_data: dict) -> []:
            properties = []
            for name, value in device_data.items():
                if name == 'temperature':
                    properties.append({
                        "type": "devices.properties.float",
                        "state": {
                            "instance": "temperature",
                            "value": value
                        }
                    })
                elif name == 'humidity':
                    properties.append({
                        "type": "devices.properties.float",
                        "state": {
                            "instance": "humidity",
                            "value": value
                        }
                    })
                elif name == 'battery':
                    properties.append({
                        "type": "devices.properties.float",
                        "state": {
                            "instance": "battery_level",
                            "value": value
                        }
                    })
            return properties

        device_data_list = [get_device_data(request_device['id']) for request_device in data['devices']]

        res = {
            "request_id": request_id,
            "payload": {
                "devices": [{
                    "id": device_data['request_device_id'],
                    "capabilities": map_capabilities(device_data['device_data']),
                    "properties": map_properties(device_data['device_data'])
                } for device_data in device_data_list]
            }
        }

        return res

    def action_devices(self, request_id: str, data: dict):
        def process_capabilities(request_device: dict):
            request_device_id = request_device['id']
            cfg_device = self._get_cfg_device_by_yandex_id(request_device_id)
            cfg_device_name = cfg_device['name']

            result_capabilities = []
            for capability in request_device['capabilities']:

                cap_type = capability['type']
                instance = capability['state']['instance']
                value = capability['state']['value']

                result_cap = {
                    "type": cap_type,
                    "state": {
                        "instance": instance,
                        "action_result": {
                            "status": "ERROR"
                        }
                    }
                }

                if cap_type == 'devices.capabilities.on_off' and instance == 'on':
                    self.device_client.set_switch_state(cfg_device_name, value)
                    result_cap['state']['action_result']['status'] = 'DONE'

                result_capabilities.append(result_cap)

            return dict(request_device_id=request_device_id, capabilities=result_capabilities)

        device_capabilities_list = map(process_capabilities, data['payload']['devices'])

        res = {
            "request_id": request_id,
            "payload": {
                "devices": [{
                    "id": device_capabilities['request_device_id'],
                    "capabilities": device_capabilities['capabilities']
                } for device_capabilities in device_capabilities_list]
            }
        }

        return res

    @staticmethod
    def _get_cfg_device_by_yandex_id(yandex_device_id: str) -> dict:
        return [device for device in config.DEVICES if device['yandex_data']['id'] == yandex_device_id][0]
