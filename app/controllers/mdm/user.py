

class User(object):
    def __init__(self, mail, user_id, name):
        self.mail = mail
        self.id = user_id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.id}:{self.name}"
