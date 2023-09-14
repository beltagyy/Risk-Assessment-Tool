#forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired(), validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=8, max=80)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired(), validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')
