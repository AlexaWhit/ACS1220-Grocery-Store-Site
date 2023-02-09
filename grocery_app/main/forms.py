from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, Length, ValidationError
from grocery_app.models import *
from grocery_app.extensions import bcrypt

class GroceryStoreForm(FlaskForm):
    title = StringField('Store Title', validators=[DataRequired()])
    address = StringField('Address')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete Store')

class GroceryItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=ItemCategory.choices())
    photo_url = StringField('Photo', validators=[DataRequired()])
    store = QuerySelectField('Stores', query_factory=lambda: GroceryStore.query)
    submit = SubmitField('Submit')
    delete = SubmitField('Delete Item')

class UserForm(FlaskForm):
    """Form to create a user."""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit User')



