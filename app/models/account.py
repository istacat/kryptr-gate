import secrets
import string
from datetime import datetime
from sqlalchemy.orm import relationship

from app import db
from app.models.utils import ModelMixin


class Account(db.Model, ModelMixin):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    ecc_id = db.Column(db.String(7), nullable=False, unique=True)
    ad_login = db.Column(db.String(32), nullable=False)
    ad_password = db.Column(db.String(32), nullable=False)
    license_key = db.Column(db.String(64), nullable=True)
    email = db.Column(
        db.String(32), nullable=False, unique=True
    )  # automatically generated
    reseller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reseller = relationship("User")
    subscriptions = relationship("Subscription", viewonly=True)
    sim = db.Column(db.String(20))
    comment = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    mdm_device_id = db.Column(db.String(10))

    def to_json(self):
        return {
            "id": self.id,
            "ecc_id": self.ecc_id,
            "ad_password": self.ad_password,
            "license_key": self.license_key,
            "email": self.email,
            "reseller_id": self.reseller_id,
            "reseller": self.reseller.username,
            # "subscriptions": self.subscriptions,
            "sim": self.sim,
            "created_at": self.created_at,
            "comment": self.comment
        }

    @staticmethod
    def gen_ecc_id():
        ecc_id = ecc_sample_gen()
        while Account.query.filter(Account.ecc_id == ecc_id).first():
            ecc_id = ecc_sample_gen()
        return ecc_id


def ecc_sample_gen() -> str:
    ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ"+string.digits
    while True:
        password = ''.join(secrets.choice(ALPHABET) for i in range(7))
        if (sum(c.isalpha() for c in password) >= 3
                and sum(c.isdigit() for c in password) >= 3):
            return password
