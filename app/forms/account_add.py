from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.core import DateField, SelectField
from wtforms.validators import DataRequired, Length, Email
from app.models import User


class AccountAddForm(FlaskForm):
    def __init__(self, user=None):
        super().__init__()
        if user:
            if (
                current_user.role.name == "distributor"
                or current_user.role.name == "reseller"
            ):
                self.reseller.choices = [sub.username for sub in current_user.subs]
            elif current_user.role.name == "sub_reseller":
                self.reseller.choices = [current_user.username]
            else:
                users = User.query.filter(User.deleted == False) # noqa E712
                self.reseller.choices = [sub.username for sub in users]

    reseller = SelectField("Reseller", choices=[])
    sub_duration = SelectField("Subscription", choices=[
        (1, '1 Month'),
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '12 Months')
    ], default=1)
    sub_activate_date = DateField("Activation Date")
    plus = SubmitField(label="+")
    submit = SubmitField(label="Save")


class NewAccountForm(FlaskForm):
    ecc_id = StringField("Ecc ID", [DataRequired(), Length(min=7, max=7)])
    ecc_password = StringField("ECC Password", [DataRequired()])
    ad_login = StringField("Login", [DataRequired()])
    ad_password = StringField("AD Password", [DataRequired()])
    email = StringField("Email", [DataRequired(), Email(5, 45)])
    sim = StringField("Sim")
    comment = TextAreaField("Comments")
    submit = SubmitField("Invisible submit")
