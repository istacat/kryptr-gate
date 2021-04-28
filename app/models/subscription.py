from datetime import datetime
from sqlalchemy.orm import relationship
from .utils import ModelMixin

from app import db


class Subscription(db.Model, ModelMixin):

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    activation_date = db.Column(db.Date)
    type = db.Column(db.String(32), default='new')
    months = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    account = relationship("Account")
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    account = relationship("Account")
    created_at = db.Column(db.DateTime, default=datetime.now)
