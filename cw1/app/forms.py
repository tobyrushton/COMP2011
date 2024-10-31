from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired

class AssessmentForm(FlaskForm):
    module_code = StringField('module_code', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    due_date = DateTimeLocalField('deadline', validators=[DataRequired()])