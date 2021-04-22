from .base import post, get


class DeviceAction(object):
    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name

    @property
    def status(self):
        return get(f"device/{self.device_id}/actions/{self.name}")

    def run(self):
        return post(f"device/{self.device_id}/actions/{self.name}")
