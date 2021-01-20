from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    product_name = StringField("Product Name", [DataRequired()])
    comment = TextAreaField("Comment", [DataRequired()])

    submit = SubmitField()
