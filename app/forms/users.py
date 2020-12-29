from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    activated = SelectField(
        "Activated",
        default="active",
        choices=[("not_active", "Not Active"), ("active", "Active")],
    )
    role = SelectField(
        "User type",
        default="support",
        choices=[
            ("admin", "Admin"),
            ("distributor", "Distributor"),
            ("reseller", "Reseller"),
            ("sub_reseller", "Sub Reseller"),
            ("support", "Support"),
        ],
    )
