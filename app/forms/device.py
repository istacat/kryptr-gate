from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class DeviceForm(FlaskForm):

    complete_wipe = SelectField(
        "Complete Wipe",
        default="pass",
        choices=[("pass", "Pass"), ("run", "Run Command")],
    )
    submit = SubmitField()
