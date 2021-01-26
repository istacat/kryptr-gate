from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    activated = SelectField(
        "Activated",
        default="active",
        choices=[("active", "Active"), ("not_active", "Not Active")],
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
    submit = SubmitField()
