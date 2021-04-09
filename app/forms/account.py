from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from app.models import User


class AccountForm(FlaskForm):

    def get_users():
        return User.query.filter(User.deleted == False).filter(~User.role.in_(['admin', 'support'])) # noqa E712

    ecc_id = StringField("Ecc", [DataRequired(), Length(min=6, max=6)])
    email = StringField("Email", [DataRequired(), Email(3, 45)])
    ad_login = StringField("Login", [DataRequired()])
    ad_password = StringField("Password", [DataRequired()])
    sim = StringField("Sim")
    comment = TextAreaField("Comments")
    reseller = QuerySelectField("Reseller", query_factory=get_users, allow_blank=True)
    submit = SubmitField()
