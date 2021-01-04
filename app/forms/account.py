from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class AccountForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    ecc_id = StringField("Ecc", [DataRequired(), Length(min=6, max=6)])
    email = StringField("Email", [DataRequired(), Email(3, 45)])
    ad_login = StringField("Login", [DataRequired()])
    ad_password = PasswordField("Password", [DataRequired()])
    license_key = StringField("License", [DataRequired()])
    sim = StringField("Sim")
    imei = StringField("IMEI")
    comment = TextAreaField("Comments")

    submit = SubmitField()
