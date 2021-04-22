

class Group(object):
    def __init__(self, group_id: str = None, data: dict = None):
        self.data = data if data else None
        self.group_id = data["group_id"] if data else group_id

    @property
    def name(self) -> str:
        return self.data["name"]
