from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class LogInForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=16, message='Password must be between 8 and 16 characters.')])

class SignUpForm(LogInForm):
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])

class CreatePostForm(FlaskForm):
    body = StringField('body', validators=[DataRequired(), Length(min=1, max=256)])

