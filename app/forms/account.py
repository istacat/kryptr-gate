from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email
from app.controllers import ALL_USERS


class AccountForm(FlaskForm):
    ecc_id = StringField("Ecc", [DataRequired(), Length(min=6, max=6)])
    email = StringField("Email", [DataRequired(), Email(3, 45)])
    ad_login = StringField("Login", [DataRequired()])
    ad_password = StringField("Password", [DataRequired()])
    sim = StringField("Sim")
    comment = TextAreaField("Comments")
    reseller = SelectField("Reseller", choices=ALL_USERS)
    submit = SubmitField()
