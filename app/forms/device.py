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
            ("remote_alarm", "Remote Alarm"),
            ("scan", "Scan Now"),
            ("lock", "Remote Lock"),
            ("corporate_wipe", "Corporate Wipe"),
            ("complete_wipe", "Complete Wipe"),
            ("clear_passcode", "Clear Passcode"),
            ("reset_passcode", "Reset Passcode"),
            ("fetch_location", "Locate Device"),
            ("enable_lost_mode", "Enable Lost Mode"),
            ("restart", "Restart Device"),
            ("remote_debug", "Request Bug Report"),
        ],
    )
    submit = SubmitField("Run")
