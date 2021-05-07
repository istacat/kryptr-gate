import json
import requests
from requests.auth import HTTPBasicAuth
from config import BaseConfig as conf
from app.logger import log


class SimPro:
    def __init__(self):
        self.base_url = conf.SIMPRO_BASE_URL
        self.basic_auth = HTTPBasicAuth(conf.SIMPRO_USERNAME, conf.SIMPRO_PASSWORD)
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def check_sim(self, iccid):
        allow_sim = False
        for sim in self.sims:
            if sim["iccid"] == str(iccid) and sim["status"] == "inactive":
                allow_sim = True
                break
        return allow_sim

    @property
    def sims(self):
        sims = []
        page = 1
        while True:
            response = requests.get(
                url=self.base_url + "/api/v3/sims",
                auth=self.basic_auth,
                headers=self.headers,
                params={"page": page, "limit": 300},
            )
            if "does not exist" in response.text:
                break
            sims.extend(json.loads(response.text)["sims"])
            page += 1
        return [{"iccid": sim["iccid"], "status": sim["status"]} for sim in sims]

    @property
    def customer_solutions(self):
        response = requests.get(
            url=self.base_url + "/api/v3/customer-solutions",
            auth=self.basic_auth,
            headers=self.headers,
        )
        return response

    def bar_sim(self, iccid):
        response = requests.post(
            url=self.base_url + "/api/v3/sims/bars",
            auth=self.basic_auth,
            headers=self.headers,
            data=json.dumps(
                {
                    "identifiers": [str(iccid)],
                    "bar_name": "full_bar",
                    "required_state": True,
                }
            ),
        )
        if response.status_code != 200:
            return None
        return True

    def activate_sim(self, iccid):
        response = requests.post(
            url=self.base_url + "/api/v3/sims/activation",
            auth=self.basic_auth,
            headers=self.headers,
            data=json.dumps({"iccids": [str(iccid)]}),
        )
        if response:
            return None
        return True

    def calncel_sim(self, iccid):
        response = requests.post(
            url=self.base_url + "/api/v3/sims/activation",
            auth=self.basic_auth,
            headers=self.headers,
            data=json.dumps(
                {
                    "items": [
                        {
                            "identifier": [str(iccid)],
                            "cancelation_date": "2021-05-07",
                            "enable_full_bar": True,
                        }
                    ],
                    "pre_approved": True,
                }
            ),
        )
        if response:
            return None
        return True

    def sim_info(self, iccid):
        response = requests.get(
                url=self.base_url + "/api/v3/sims/details",
                auth=self.basic_auth,
                headers=self.headers,
                params={"identifiers": iccid},
            )
        if response:
            return True
        return True
