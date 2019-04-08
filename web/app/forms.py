from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, IntegerField, validators, FileField, \
    MultipleFileField, SelectField, RadioField
from wtforms.validators import DataRequired


# Structure of the Login form
class LoginForm(Form):
    email = StringField('Email', [
        validators.DataRequired(message='Es necesario introducir un email')])
    password = PasswordField('Contraseña', [
        validators.DataRequired(message='Es necesario una contraseña')])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Iniciar Sesión')


# Structure of the Register form
class RegisterForm(Form):
    name = StringField('Nombre', [
        validators.DataRequired(message='Es necesario introducir un nombre'),
        validators.Length(min=4, max=50, message='El tamaño máximo del nombre son 50 carácteres')])
    lastname = StringField('Apellidos', [
        validators.DataRequired(message='Es necesario introducir apellidos'),
        validators.Length(min=4, max=50, message='El tamaño máximo del nombre son 50 carácteres')])

    # username = StringField('Username', [
    #    validators.Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 carácteres')])
    email = StringField('Email', [
        validators.DataRequired(message='Es necesario introducir un email'),
        validators.Length(min=1, max=50, message='El email no puede contener más de 50 carácteres')])
    password = PasswordField('Contraseña', [
        validators.DataRequired(message='Es necesario una contraseña'),
        validators.Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    confirm = PasswordField('Confirmar Contraseña', [
        validators.EqualTo('password', message='Las contraseñas no coinciden')
    ])


class EditProfile(Form):
    name = StringField('Nombre', [
        validators.DataRequired(message='Es necesario introducir un nombre'),
        validators.Length(min=4, max=50, message='El tamaño máximo del nombre son 50 carácteres')])
    lastname = StringField('Apellidos', [
        validators.DataRequired(message='Es necesario introducir apellidos'),
        validators.Length(min=4, max=50, message='El tamaño máximo del nombre son 50 carácteres')])

    # username = StringField('Username', [
    #    validators.Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 carácteres')])
    email = StringField('Email', [
        validators.DataRequired(message='Es necesario introducir un email'),
        validators.Length(min=1, max=50, message='El email no puede contener más de 50 carácteres')])
    password = PasswordField('Contraseña', [
        validators.DataRequired(message='Es necesario una contraseña'),
        validators.Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    confirm = PasswordField('Confirmar Contraseña', [
        validators.EqualTo('password', message='Las contraseñas no coinciden')
    ])
    genero = RadioField('Genero', choices = [('hombre','Hombre'),('mujer','Mujer')])


# Structure of the Subir Anuncio form
class SubirAnuncioForm(Form):
    images = MultipleFileField('Imagenes')
    productName = StringField('Nombre del producto', [
        validators.DataRequired(message='Es necesario introducir un nombre de producto'),
        validators.Length(min=1, max=50, message='El tamaño máximo del nombre del producto son 50 carácteres')])
    productPrice = StringField('Precio (€)', [
        validators.DataRequired(message='Es necesario introducir un precio'),
        validators.Length(min=1, max=10, message='El tamaño máximo del precio del producto son 10 números')])
    productCategory = StringField('Categoría', [
        validators.DataRequired(message='Es necesario seleccionar una categoría')])
    productDescription = StringField('Descripción detallada', [
        validators.DataRequired(message='Es necesario escribir una descripción')])
    productLong = StringField('Longitud', [
        validators.DataRequired(message='Es necesario introducir una longitud'),
        validators.Length(min=1, max=10, message='El tamaño máximo de la longitud son 10 números')])
    productLat = StringField('Latitud', [
        validators.DataRequired(message='Es necesario introducir una latitud'),
        validators.Length(min=1, max=10, message='El tamaño máximo de la latitud son 10 números')])
