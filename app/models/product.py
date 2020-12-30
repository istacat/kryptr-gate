from sqlalchemy.orm import relationship

from app import db


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    subscriptions = relationship("Subscription")
    comment = db.Column(db.String(200))
