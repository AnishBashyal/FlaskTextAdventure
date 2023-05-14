from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired

class CreateStoryForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    theme = StringField('Theme', validators = [DataRequired()])
    submit = SubmitField('Create')


class BuildStoryForm(FlaskForm):
    story = TextAreaField('Story', validators = [DataRequired()])
    submit = SubmitField('Update')
    is_last = RadioField(choices = [('win', 'Is Win?'), ('lose', 'Is Lose?'), ('none', 'None')], default='none')

class BuildOptionForm(FlaskForm):
    option = TextAreaField('Option', validators = [DataRequired()])
    submit = SubmitField('Add')