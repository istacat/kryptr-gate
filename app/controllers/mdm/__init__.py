from .device import Device
from .group import Group
from .base import get_list_of


class MDM:
    def __init__(self) -> None:
        pass

    @property
    def devices(self):
        # result = get("devices")
        devices = get_list_of("devices", "devices")
        return [Device(data=data) for data in devices]

    @property
    def groups(self):
        return [Group(data=data) for data in get_list_of("groups", "groups")]
