from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, IntegerField, validators, FileField, \
    MultipleFileField, SelectField, RadioField, HiddenField, DecimalField, TextAreaField
from wtforms.fields.html5 import DateField
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

class EditPicture(FlaskForm):
    picture = FileField('Imagen de perfil')
    submit = SubmitField('Establecer imagen')
    delete = SubmitField('Eliminar imagen')

# Structure of the Subir Anuncio form
class SubirAnuncioForm(FlaskForm):
    # pictures = HiddenField("Imágenes")
    # mimes = HiddenField("Formatos de imagen")
    name = StringField('Nombre del producto', [
        validators.DataRequired(message='Es necesario introducir un nombre de producto'),
        validators.Length(min=1, max=50, message='El tamaño máximo del nombre del producto son 50 carácteres')])
    price = DecimalField('Precio (€)', [
        validators.DataRequired(message='Es necesario introducir un precio'),
        validators.NumberRange(min=0, max=1000000, message='El precio intoducido no es válido (de 0 € a 999.999,99 €)')])
    category = SelectField('Categoría', 
        choices = [ 
            ('Automoción', 'Automoción'),
            ('Informática', 'Informática'),
            ('Moda', 'Moda'),
            ('Deporte y ocio', 'Deporte y ocio'),
            ('Videojuegos', 'Videojuegos'),
            ('Libros y música', 'Libros y música'),
            ('Hogar y jardín', 'Hogar y jardín'),
            ('Foto y audio ', 'Foto y audio ')
        ], validators = [ 
            validators.DataRequired(message='Es necesario seleccionar una categoría') ])
    description = TextAreaField('Descripción', [
        validators.DataRequired(message='Es necesario escribir una descripción')])
    lat = HiddenField('Latitud', [
        validators.DataRequired(message='No se ha podido obtener la nueva localización')])
    lng = HiddenField('Longitud', [
        validators.DataRequired(message='No se ha podido obtener la nueva localización')])
    enddate = DateField('End', format = '%Y-%m-%d', description = 'Time that the event will occur',
        validators= [validators.Optional()] )
    submit = SubmitField('Publicar Anuncio')


class ProductSearch(Form):
    categories = ['Automoción', 'Informática', 'Moda', 'Deporte y ocio', 'Videojuegos', 'Libros y música', 'Hogar y jardín', 'Foto y audio']
    category = SelectField('Categoría', 
        choices = [ 
            ('Automoción', 'Automoción'),
            ('Informática', 'Informática'),
            ('Moda', 'Moda'),
            ('Deporte y ocio', 'Deporte y ocio'),
            ('Videojuegos', 'Videojuegos'),
            ('Libros y música', 'Libros y música'),
            ('Hogar y jardín', 'Hogar y jardín'),
            ('Foto y audio ', 'Foto y audio ')
        ])
    estados = [('en venta', 'En Venta'), ('vendido', 'Vendido')]
    resultadosporpag = ['15', '30', '45', '60', '75', '90']
    ordenacionlist = [('published ASC', 'Fecha (Más viejos primero)'), ('published DESC', 'Fecha (Más nuevos primero)'), ('distance DESC', 'Distancia Descendente'), ('distance ASC', 'Distancia Ascendente'), ('price ASC', 'Precio Ascendente'), ('price DESC', 'Precio Descendente')]
    status = SelectField('Estado',
            choices = [
                ('en venta','En Venta'),
                ('vendido','Vendido')
            ])
    keywords = StringField('Palabras Clave')
    minprice = StringField('Precio Mínimo')
    maxprice = IntegerField('Precio Máximo')
    minpublished = DateField('Start', format = '%Y-%m-%d', description = 'Time that the event will occur')
    maxpublished = DateField('Start', format = '%Y-%m-%d', description = 'Time that the event will occur')
    resultados = SelectField('Resultados Por Página',
            choices = [
                ('15', '15'),
                ('30', '30'),
                ('45', '45'),
                ('60', '60'),
                ('75', '75'),
                ('90', '90')
            ])
    ordenacion = SelectField('Ordenación de Resultados',
            choices = [
                ('published ASC', 'Fecha (Más viejos primero)'),
                ('published DESC', 'Fecha (Más nuevos primero)'),
                ('distance DESC', 'Distancia Descendente'),
                ('distance ASC', 'Distancia Ascendente'),
                ('price ASC', 'Precio Ascendente'),
                ('price DESC', 'Precio Descendente')
            ])
    distancia = StringField('Distancia')
    submit = SubmitField('Buscar')

class Review(FlaskForm):
    stars = IntegerField('Puntuación', [
        validators.DataRequired(message='Es necesario introducir una puntuación entre 1 y 5'),
        validators.NumberRange(min=1, max=5, message='La puntuación debe ser de 1 a 5 estrellas')])
    comment = TextAreaField('Comentario', [
        validators.DataRequired(message='Es necesario escribir un comentario')])
    submit = SubmitField('Publicar Valoración')


class bidPlacementForm(FlaskForm):
    amount = IntegerField('Cantidad')
    submit = SubmitField('Realizar Puja')

class reportForm(Form):
    category = SelectField('Categoría', 
        choices = [ 
            ('Sospecha de fraude', 'Sospecha de fraude'),
            ('No acudió a la cita', 'No acudió a la cita'),
            ('Mal comportamiento', 'Mal comportamiento'),
            ('Artículo defectuoso', 'Artículo defectuoso'), 
            ('Otros', 'Otros')])
    description = TextAreaField('Descripción del informe', [
        validators.DataRequired(message='Es necesario escribir una descripción')])
    submit = SubmitField('Publicar Informe')
