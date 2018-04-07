from flask_login import current_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class SettingsForm(Form):
    firstname = StringField('First Name', render_kw={'class': 'form-control', 'placeholder': 'John', 'required': True}, validators=[DataRequired('How should be call you? Please enter your first name.')])
    lastname = StringField('Last Name', render_kw={'class': 'form-control', 'placeholder': 'Doe', 'required': True}, validators=[DataRequired('How should be call you? Please enter your last name.')])
    email = EmailField('Email', render_kw={'class': 'form-control', 'placeholder': 'john@doe.com', 'required': True}, validators=[DataRequired('Please enter a valid email address.'), Email()])
    submit = SubmitField('Update', render_kw={'class': 'btn btn-primary btn-round'} )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            if current_user.is_anonymous:
                raise ValidationError('Please use a different email address.')
            elif user.email != current_user.email:
                raise ValidationError('Please use a different email address.')