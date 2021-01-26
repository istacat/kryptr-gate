from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired


class DistributorForm(FlaskForm):
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
        default="distributor",
        choices=[
            ("distributor", "Distributor"),
        ],
    )
    submit = SubmitField()
