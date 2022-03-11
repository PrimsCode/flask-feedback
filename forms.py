from ast import Pass
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Your Feedback", validators=[InputRequired()])