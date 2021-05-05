import json
import requests
from requests.auth import HTTPBasicAuth
from config import BaseConfig as conf


class SimPro:
    def __init__(self):
        self.base_url = conf.SIMPRO_BASE_URL
        self.basic_auth = HTTPBasicAuth(conf.SIMPRO_USERNAME, conf.SIMPRO_PASSWORD)
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def check_sim(self, iccid):
        allow_sim = False
        for sim in self.sims:
            if sim['iccid'] == str(iccid) and sim['status'] == 'inactive':
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
