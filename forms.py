from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo


# Create class for register
class RegisterForm(FlaskForm):
    # Get each field in form and validate it
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password= PasswordField('Password', validators=[InputRequired(), Length(min=12)])
    password_confirm = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=12), EqualTo('password')])
    submit = SubmitField('Register')


# Create class for login
class LoginForm(FlaskForm):
    # Get each field in form and validate it
    name = StringField('name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=12)])
    submit = SubmitField('Login')


#Create class for search
class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[InputRequired()])
    submit_search = SubmitField('Search')