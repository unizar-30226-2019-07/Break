from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, IntegerField, validators, FileField, \
    MultipleFileField, SelectField, RadioField, HiddenField
from wtforms.validators import DataRequired


# Structure of the Login form
class LoginForm(Form):
    email = StringField('Email', [
        validators.DataRequired(message='Es necesario introducir un email')])
    password = PasswordField('Contraseña', [
        validators.DataRequired(message='Es necesario introducir una contraseña')])
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


class EditProfile(FlaskForm):
    name = StringField('Nombre', [
        validators.DataRequired(message='Es necesario introducir un nombre'),
        validators.Length(min=4, max=50, message='El tamaño máximo del nombre son 50 carácteres')])
    lastname = StringField('Apellidos', [
        validators.DataRequired(message='Es necesario introducir apellidos'),
        validators.Length(min=4, max=50, message='El tamaño máximo del nombre son 50 carácteres')])
    gender = RadioField('Género', choices = [('hombre','Hombre'),('mujer','Mujer')])
    submit = SubmitField('Guardar cambios')

class EditLocation(FlaskForm):
    lat = HiddenField('Latitud', [
        validators.DataRequired(message='No se ha podido obtener la nueva localización')
    ])
    lng = HiddenField('Longitud', [
        validators.DataRequired(message='No se ha podido obtener la nueva localización')
    ])
    submit = SubmitField('Establecer ubicación')

class EditPassword(FlaskForm):
    password = PasswordField('Eliga una contraseña', [
        validators.DataRequired(message='Es necesario introducir una contraseña'),
        validators.Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    confirm = PasswordField('Confirme la contraseña', [
        validators.EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Cambiar contraseña')

class EditEmail(FlaskForm):
    email = StringField('Correo electrónico', [
        validators.DataRequired(message='Es necesario introducir una dirección de correo'),
        validators.Length(min=1, max=50, message='El correo no puede contener más de 50 carácteres')])
    confirm = StringField('Confirmar correo electrónico', [
        validators.EqualTo('email', message='Los correos no coinciden')
    ])
    submit = SubmitField('Cambiar correo')

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


class ProductSearch(Form):
    category = StringField('Categoría')
    type = StringField('Tipo')
    keywords = StringField('Palabras Clave')
    minprice = StringField('Precio Mínimo')
    maxprice = StringField('Precio Máximo')
    minpublished = StringField('Fecha Mínima de Publicación')
    maxpublished = StringField('Fecha Máxima de Publicación')
    submit = SubmitField('Buscar')

