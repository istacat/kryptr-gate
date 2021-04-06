from datetime import datetime
from sqlalchemy.orm import relationship

from app import db
from app.models.utils import ModelMixin


class Account(db.Model, ModelMixin):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    ecc_id = db.Column(db.String(6), nullable=False, unique=True)
    ad_login = db.Column(db.String(32), nullable=False)
    ad_password = db.Column(db.String(32), nullable=False)
    license_key = db.Column(db.String(64), nullable=True)
    email = db.Column(
        db.String(32), nullable=False, unique=True
    )  # automatically generated
    reseller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reseller = relationship("User")
    subscriptions = relationship("Subscription")
    sim = db.Column(db.String(20))
    comment = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

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
