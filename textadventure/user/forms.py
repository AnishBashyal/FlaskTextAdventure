from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from textadventure.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("User name already taken")


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAcccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=3, max=30)])
    profile_pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user and user!= current_user:
            raise ValidationError("User name already taken")
    
        