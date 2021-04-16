from datetime import datetime
import enum

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin
from app.models.subordinate import Subordinate
from app.models.account import Account


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    class RoleType(enum.Enum):
        """Utility class to support
        Support - maintain accounts (excluding creating/deleting)
        Sub_reseller - can create and manage own accounts
        Reseller - can manage sub_ressellers and manage own accounts + sub_resseler's
        Distributor - can manage resellers
        Admin - super user
        """

        support = 1
        sub_reseller = 2
        reseller = 3
        distributor = 4
        admin = 5

    class StatusType(enum.Enum):
        active = "Active"
        not_active = "Not active"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(256))
    password_hash = db.Column(db.String(255), nullable=False)
    activated = db.Column(Enum(StatusType), default=StatusType.active)
    role = db.Column(Enum(RoleType), default=RoleType.support)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "activated": self.activated.name,
            "role": self.role.name,
            "created_at": self.created_at,
        }

    @property
    def subs(self):
        """Get all users subordinates"""
        if self.role.name == "distributor":
            users = [self]
            for user in self.resellers:
                users.append(user)
            for user in self.sub_resellers:
                users.append(user)
            return users
        elif self.role.name == "reseller":
            users = [self]
            for user in self.sub_resellers:
                users.append(user)
            return users

    @property
    def chief(self):
        """Get users chief"""
        if self.role.name in ("reseller", "sub_reseller"):
            sub = Subordinate.query.filter(
                Subordinate.subordinate_id == self.id
            ).first()
            if not sub:
                return None
            chief = User.query.get(sub.chief_id)
            return chief

    @property
    def distributors(self):
        """Get all distributors for admin"""
        if self.role.name == "admin":
            return User.query.filter(User.role == "distributor")

    @property
    def resellers(self):
        """Get resellers by roles and subordinates"""
        if self.role.name == "admin":
            users = User.query.filter(User.role == "reseller")
            return users
        elif self.role.name == "distributor":
            users = []
            subs = Subordinate.query.filter(Subordinate.chief_id == self.id)
            for relation in subs:
                user = User.query.get(relation.subordinate_id)
                if user.role.name == "reseller":
                    users.append(user)
            return users

    @property
    def sub_resellers(self):
        """Get sub_resellers by roles and subordinates"""
        users = []
        if self.role.name == "admin":
            users = User.query.filter(User.role == "sub_reseller")
            return users
        elif self.role.name == "distributor":
            for reseller in self.resellers:
                new_query = Subordinate.query.filter(
                    Subordinate.chief_id == reseller.id
                )
                for relation in new_query:
                    user = User.query.get(relation.subordinate_id)
                    users.append(user)
            subs = Subordinate.query.filter(Subordinate.chief_id == self.id)
            for relation in subs:
                user = User.query.get(relation.subordinate_id)
                if user.role.name == "sub_reseller":
                    users.append(user)
            return users
        elif self.role.name == "reseller":
            subs = Subordinate.query.filter(Subordinate.chief_id == self.id)
            for relation in subs:
                user = User.query.get(relation.subordinate_id)
                users.append(user)
            return users

    @property
    def accounts(self):
        return get_accounts(self)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter(
            db.or_(cls.username == user_id, cls.email == user_id)
        ).first()
        if user is not None and check_password_hash(user.password, password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.username}>"

    def __str__(self):
        return self.username


def get_accounts(user):
    """Get accounts by roles and subordinates"""
    if user.role.name == "admin" or user.role.name == "support":
        return Account.query.all()
    elif user.role.name == "distributor":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        for reseller in user.resellers:
            for account in Account.query.filter(Account.reseller_id == reseller.id):
                accounts.append(account)
        for sub_reseller in user.sub_resellers:
            for account in Account.query.filter(Account.reseller_id == sub_reseller.id):
                accounts.append(account)
        return accounts
    elif user.role.name == "reseller":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        for sub_reseller in user.sub_resellers:
            for account in Account.query.filter(Account.reseller_id == sub_reseller.id):
                accounts.append(account)
        return accounts
    elif user.role.name == "sub_reseller":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        return accounts


class AnonymousUser(AnonymousUserMixin):
    pass
