from flask_login import current_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User

class PasswordForm(Form):
    currentpassword = PasswordField('Current Password', render_kw={'class': 'form-control', 'placeholder': 'enter current password', 'required': True}, validators=[DataRequired('Please enter your current password.')])
    confirmpassword = PasswordField('Re-Enter Current Password', render_kw={'class': 'form-control', 'placeholder': 're-enter your password', 'required': True}, validators=[DataRequired(), EqualTo('currentpassword')])
    newpassword = PasswordField('Password', render_kw={'class': 'form-control', 'placeholder': '6+ characters', 'required': True, 'pattern': '.{6,}', 'title': 'Minimum 6 characters'}, validators=[DataRequired('Please enter a new password.')])
    submit = SubmitField('Update Password', render_kw={'class': 'btn btn-primary btn-round'} )