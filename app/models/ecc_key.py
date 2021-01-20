from sqlalchemy.orm import relationship

from app import db
from app.models.utils import ModelMixin


class EccKey(db.Model, ModelMixin):
    """
    Table is used for counting, never delete rows
    """

    __tablename__ = "ecc_keys"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account")
