from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from textadventure.models import User

class CreateStoryForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    theme = StringField('Theme', validators = [DataRequired()])
    submit = SubmitField('Create')


class BuildStoryForm(FlaskForm):
    story = TextAreaField('Story', validators = [DataRequired()])
    submit = SubmitField('Save')

class BuildOptionForm(FlaskForm):
    option = TextAreaField('Option', validators = [DataRequired()])
    submit = SubmitField('Save')