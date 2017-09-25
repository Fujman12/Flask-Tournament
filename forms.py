from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    remember_me = BooleanField('Remember me')


class SignUpForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid e-mail')])
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=20)])
    first_name = StringField('First name', validators=[InputRequired(), Length(min=3, max=40)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=3, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password')