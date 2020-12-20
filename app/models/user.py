from datetime import datetime
import enum

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = 'users'

    class RoleType(enum.Enum):
        """Utility class to support"""
        support = 1
        sub_reseller = 2
        reseller = 3
        distributor = 4
        admin = 5

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, default=False)
    role = db.Column(Enum(RoleType), default=RoleType.support)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter(db.or_(cls.username == user_id, cls.email == user_id)).first()
        if user is not None and check_password_hash(user.password, password):
            return user

    def __str__(self):
        return '<User: %s>' % self.username


class AnonymousUser(AnonymousUserMixin):
    pass
