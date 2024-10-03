from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    firstname = StringField('first name', validators=[DataRequired()])
    lastname = StringField('last name', validators=[DataRequired()])
    phone = StringField('phone number', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField('Register')