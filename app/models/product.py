from sqlalchemy.orm import relationship

from app import db
from app.models.utils import ModelMixin


class Product(db.Model, ModelMixin):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    subscriptions = relationship("Subscription")
    comment = db.Column(db.String(200))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "comment": self.comment
        }
