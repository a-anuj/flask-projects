from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import data_required, EqualTo
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    name = StringField("Name", validators=[data_required()])
    username = StringField("Username", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    color = StringField("Favorite color")
    submit = SubmitField("Submit")
    password_hash = PasswordField("Password", validators=[data_required(), EqualTo('password_hash2')])
    password_hash2 = PasswordField("Confirm Password", validators=[data_required()])


class SimpleForm(FlaskForm):
    name = StringField("What's your name", validators=[data_required()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email = StringField("What's your email", validators=[data_required()])
    password_hash = PasswordField("What's your password", validators=[data_required()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[data_required()])
    content = StringField("Content", validators=[data_required()], widget=TextArea())
    author = StringField("Author")
    slug = StringField("Slug", validators=[data_required()])
    submit = SubmitField("Submit", validators=[data_required()])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[data_required()])
    password = PasswordField("Password", validators=[data_required()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[data_required()])
    submit = SubmitField("Submit")