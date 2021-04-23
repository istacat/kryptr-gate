from .base import get_list_of
from .device_action import DeviceAction


class Device(object):
    def __init__(self, device_id: str = None, data: dict = None):
        self.data = data if data else None
        self.device_id = data["device_id"] if data else device_id
        self.account = data['user']['user_name'] if 'user' in data else None

    @property
    def actions(self) -> list:
        actions = get_list_of("actions", f"devices/{self.device_id}/actions")
        return [(action["name"], action['localized_name']) for action in actions]

    def get_action(self, name):
        return DeviceAction(device_id=self.device_id, name=name)

    @property
    def name(self):
        return (
            self.data["device_name"]
            if self.data and "device_name" in self.data
            else None
        )

    @property
    def model(self):
        return self.data["model"] if self.data and "model" in self.data else None

    @property
    def serial_number(self):
        return (
            self.data["serial_number"]
            if self.data and "serial_number" in self.data
            else None
        )

    @property
    def imei(self):
        return self.data["imei"][0] if self.data and "imei" in self.data else None

    def __repr__(self) -> str:
        return f"{self.device_id}:{self.name}:{self.serial_number}:{self.imei}"
