from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(),Length(min = 6)])
    confirm_password = PasswordField('Confirm Password',
                        validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already registered. Please log in.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    cv = FileField('CV',validators = [FileAllowed(['pdf'])])
    submit = SubmitField('Upload')
class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class SmashForm(FlaskForm):
    smash = SubmitField('Smash')
    pas = SubmitField('Pass')
