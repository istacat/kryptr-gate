from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import DateField, SelectField


class SubscriptionForm(FlaskForm):
    sub_duration = SelectField("Subscription", choices=[
        (1, '1 Month'),
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '12 Months')
    ], default=1)
    sub_activate_date = DateField("Activation Date")
    submit = SubmitField("Extend Subscription")
