from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, EqualTo, Length, AnyOf, Regexp


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=15, message='Password must be between 8 and 15 characters!'),
                                                     Regexp("(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W)", message="Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit and 1 special character!")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    recaptcha = RecaptchaField("verify you are a human")
    submit = SubmitField('Log In')
