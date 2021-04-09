from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User


class SubResellerForm(FlaskForm):
    def get_users():
        return User.query.filter(User.deleted == False).filter( # noqa E712
            User.role.in_(['distributor', 'admin', 'reseller'])
        )

    username = StringField("Username", [DataRequired()])
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    activated = SelectField(
        "Activated",
        default="active",
        choices=[("not_active", "Not Active"), ("active", "Active")],
    )
    role = StringField(
        "User type",
        default="sub_reseller",
        render_kw={'readonly': True}
    )
    chief = QuerySelectField("Reseller", query_factory=get_users, allow_blank=True)
    submit = SubmitField()
