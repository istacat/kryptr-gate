from datetime import datetime

from sqlalchemy.orm import relationship

from app import db


class Subscription(db.Model):

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    activation_date = db.Column(db.DateTime, default=datetime.now)
    months = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    account = relationship("Account")
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    account = relationship("Account")
