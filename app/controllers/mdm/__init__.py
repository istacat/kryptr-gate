from .device import Device
from .group import Group
from .user import User
from .base import get_list_of, get, post
from .device_action import DeviceAction # noqa F401


class MDM:
    def __init__(self) -> None:
        pass

    def get_device(self, device_id):
        device = get(f"devices/{device_id}")
        return Device(data=device)

    @property
    def devices(self):
        devices = get_list_of("devices", "devices")
        return [Device(data=data) for data in devices]

    @property
    def groups(self):
        return [Group(data=data) for data in get_list_of("groups", "groups")]

    @property
    def users(self):
        users = get_list_of("users", "users")
        return [User(mail=user['user_email'], user_id=user['user_id'], name=user['user_name']) for user in users]

    def __getitem__(self, device_id: int) -> Device or None:
        for device in self.devices:
            if int(device.device_id) == device_id:
                return device

    def sync(self, is_full_sync=True):
        # https://mdm.kryptr.li:9383/api/v1/mdm/directory/sync
        # POST: {is_full_sync: true}
        post("directory/sync", data=dict(is_full_sync=is_full_sync))
