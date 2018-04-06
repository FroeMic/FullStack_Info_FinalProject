from flask.ext.wtf import Form
from wtforms import PasswordField, BooleanField, SubmitField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired

class LoginForm(Form):
    email = EmailField('Email', render_kw={'class': 'form-control', 'placeholder': 'john@doe.com', 'required': True}, validators=[DataRequired('Please enter a valid email address.')])
    password = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': 'your secret password', 'required': True}, validators=[DataRequired('Please enter a password.')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={'class': 'btn btn-primary btn-round'} )