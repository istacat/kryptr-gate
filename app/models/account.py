from sqlalchemy.orm import relationship

from app import db


class Account(db.Model):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    ecc_id = db.Column(db.String(6), nullable=False, unique=True)
    ad_login = db.Column(db.String(32), nullable=False)
    ad_password = db.Column(db.String(32), nullable=False)
    license_key = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(
        db.String(32), nullable=False, unique=True
    )  # automatically generated
    reseller_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    reseller = relationship("User")
    subscriptions = relationship("Subscription")
    sim = db.Column(db.String(20))
    imei = db.Column(db.String(60))
    comment = db.Column(db.String(200))
