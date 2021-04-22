from .base import post, get


class DeviceAction(object):
    def __init__(self, device_id: str, name: str):
        self.device_id = device_id
        self.name = name

    @property
    def status(self):
        return get(f"devices/{self.device_id}/actions/{self.name}")['status_description']

    def run(self):
        return post(f"devices/{self.device_id}/actions/{self.name}")

    def cancel(self):
        pass

    def __repr__(self) -> str:
        return f"{self.device_id}:{self.name}"
