import secrets
import string
import jwt
import qrcode
from config import BaseConfig as conf


def generate_password():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 1):
            return password


def create_qrcode(acc):
    """Encode ecc_id and password for chat"""
    encoded_jwt = jwt.encode({'login': acc.ecc_id, 'password': acc.ecc_password}, conf.SECRET_KEY, algorithm="HS256")
    img = qrcode.make(encoded_jwt)
    return img
