import secrets
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import relationship

from app import db
from app.models.utils import ModelMixin


class Account(db.Model, ModelMixin):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    # ECC
    ecc_id = db.Column(db.String(32), nullable=False, unique=True)
    ecc_password = db.Column(db.String(32), default=secrets.token_urlsafe(7))
    # AD
    ad_login = db.Column(db.String(32), nullable=False)
    ad_password = db.Column(db.String(32), nullable=False)

    license_key = db.Column(db.String(64), nullable=True)
    email = db.Column(
        db.String(32), nullable=False, unique=True
    )  # automatically generated
    reseller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reseller = relationship("User")
    subscriptions = relationship("Subscription", viewonly=True)
    sim = db.Column(db.String(32))
    comment = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    mdm_device_id = db.Column(db.String(32))

    def to_json(self):
        return {
            "id": self.id,
            "ecc_id": self.ecc_id,
            "activation_date": self.subscriptions[-1].activation_date.strftime(
                "%m/%d/%Y"
            ),
            "expiration_date": (
                self.subscriptions[-1].activation_date
                + relativedelta(months=+self.subscriptions[-1].months)
            ).strftime("%m/%d/%Y"),
        }

    @staticmethod
    def gen_ecc_id():
        ecc_id = ecc_sample_gen()
        while Account.query.filter(Account.ecc_id == ecc_id).first():
            ecc_id = ecc_sample_gen()
        return ecc_id

    @staticmethod
    def gen_ad_login():
        ecc_id = ecc_sample_gen()
        while Account.query.filter(Account.ad_login == ecc_id).first():
            ecc_id = ecc_sample_gen()
        return ecc_id


def ecc_sample_gen() -> str:
    ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ" + string.digits
    while True:
        password = "".join(secrets.choice(ALPHABET) for i in range(7))
        if (
            sum(c.isalpha() for c in password) >= 3
            and sum(c.isdigit() for c in password) >= 3
        ):
            return password
