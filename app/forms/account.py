from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Length, Email
from app.models import User


class AccountForm(FlaskForm):

    def __init__(self, user=None):
        super().__init__()
        if user:
            if current_user.role.name == 'distributor' or current_user.role.name == 'reseller':
                self.reseller.choices = [sub.username for sub in current_user.subs]
            elif current_user.role.name == 'sub_reseller':
                self.reseller.choices = current_user.username
            else:
                users = User.query.filter(User.deleted == False).filter(~User.role.in_(['admin', 'support'])) # noqa E712
                self.reseller.choices = [sub.username for sub in users]

    ecc_id = StringField("Ecc", [DataRequired(), Length(min=6, max=6)])
    email = StringField("Email", [DataRequired(), Email(3, 45)])
    ad_login = StringField("Login", [DataRequired()])
    ad_password = StringField("Password", [DataRequired()])
    sim = StringField("Sim")
    comment = TextAreaField("Comments")
    reseller = SelectField("Reseller", choices=[])
    submit = SubmitField()
