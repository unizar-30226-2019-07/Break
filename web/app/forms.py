from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired


# Structure of the Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Structure of the Register form
class RegisterForm(Form):
    name = StringField('Name', [
        validators.DataRequired(message='Es necesario introducir un nombre'),
        validators.Length(min=4, max=50, message='El tamaño máximo del nombre son 50 carácteres')])
    # username = StringField('Username', [
    #    validators.Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 carácteres')])
    email = StringField('Email', [
        validators.DataRequired(message='Es necesario introducir un email'),
        validators.Length(min=1, max=50, message='El email no puede contener más de 50 carácteres')])
    password = PasswordField('Password', [
        validators.DataRequired(message='Es necesario una contraseña')
    ])
    confirm = PasswordField('Confirm Password',[
        validators.EqualTo('password', message='Las contraseñas no coinciden')
    ])
