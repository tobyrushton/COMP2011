from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired, Length

class AssessmentForm(FlaskForm):
    module_code = StringField('module_code', validators=[DataRequired(), Length(min=1, max=10, message="Module code must be between 1 and 10 characters.")])
    title = StringField('title', validators=[DataRequired(), Length(min=1, max=500, message="Title must be between 1 and 100 characters.")])
    description = TextAreaField('description', validators=[DataRequired(), Length(min=1, max=500, message="Description must be between 1 and 500 characters.")])
    due_date = DateTimeLocalField('deadline', validators=[DataRequired()])