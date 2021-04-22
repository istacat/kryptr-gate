import json
import requests
from config import BaseConfig as conf


class MDM:
    def __init__(self, acc) -> None:
        self.base_url = conf.BASE_MDM_API_URL
        self.api_key = conf.MDM_API_KEY
        self.acc = acc

    def get_all_devices(self):
        response = requests.get(
            self.base_url + "/devices", headers={"Authorization": self.api_key}
        )
        return json.loads(response.content)

    def get_available_actions(self):
        response = requests.get(
            self.base_url + f"/devices/{self.acc.mdm_device_id}/actions",
            headers={"Authorization": self.api_key},
        )
        return json.loads(response.content)["actions"]

    def get_action_status(self, action):
        response = requests.get(
            self.base_url + f"/devices/{self.acc.mdm_device_id}/actions/{action}",
            headers={"Authorization": self.api_key},
        )
        return json.loads(response.content)["status_description"]

    def run_action(self, action):
        response = requests.post(
            self.base_url + f"/devices/{self.acc.mdm_device_id}/actions/{action}",
            headers={
                "Authorization": self.api_key,
                "Content-Type": "application/json;charset=UTF-8",
            }
        )
        return json.loads(response.content)

    @property
    def run_complete_wipe(self):
        return self.run_action("complete_wipe")

    @property
    def status_complete_wipe(self):
        return self.get_action_status("complete_wipe")

    @property
    def devices(self):
        return self.get_all_devices()["devices"]
