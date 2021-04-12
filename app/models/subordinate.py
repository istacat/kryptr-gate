from app import db
from app.models.utils import ModelMixin


class Subordinate(db.Model, ModelMixin):

    __tablename__ = "subordinates"

    id = db.Column(db.Integer, primary_key=True)
    chief_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    subordinate_id = db.Column(db.Integer, db.ForeignKey("users.id"))
