from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class DeviceForm(FlaskForm):

    command = SelectField(
        "Choose a command",
        [DataRequired()],
        default='',
        choices=[
            ('', ''),
        ],
    )
    submit = SubmitField("Run")
