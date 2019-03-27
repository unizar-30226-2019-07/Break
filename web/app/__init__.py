from flask import Flask, render_template, session, redirect, request, send_from_directory, flash, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from config import Config
from app.forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

# Para poder acceder a herramientas del sistema operativo
import os

# Para hacer hash de las contraseñas
from passlib.hash import sha256_crypt

import requests
import json

app = Flask(__name__)
app.config.from_object(Config)
# Database used for session management
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import models
from app.models import User

# Constante con la dirección del servidor.
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@login.user_loader
def load_user(id):
    # Required function for users to log in
    # Flask_login uses the "id" of the user in the database
    # to manage sessions
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html', auth=current_user.is_authenticated)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Check if the current user was already loged in
    if current_user.is_authenticated:
        print("Ya estabas logeado como")
        print(current_user.get_username())
        return redirect('/')
    form = LoginForm()
    if form.is_submitted():
        # TODO: hay que modificar esta función para hacer uso del token de sesión para
        # identificar la session del usuario en la tabla que hay en Flask
        # Para ello además se deberá cambiar el nombre de usuario para que deje de ser
        # único y se pasará a buscar en la tabla utilizando el token de sesión.
        print("Usuario: " + form.username.data)
        print("Contraseña: " + form.password.data)
        # Get User class of the user that is trying to log in
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            # If the user does not exist in the database that is used for sessions
            # add him to the database
            user = User(username=form.username.data)
            db.session.add(user)
            db.session.commit()
        # Use the User class to login
        # The data from remmember_me is also taken as a parameter as it will define the
        # type of the session
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Log In', form=form, auth=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    print(form.name.errors)
    print("Registro open")
    print(request.method)
    print(form.validate())
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        print("Usuario: " + username)
        print("Email: " + email)
        print("Nombre: " + name)
        print("Contraseña (sin Hash): " + form.password.data)
        print("Contraseña (con Hash): " + password)

        flash('You are now registered and can log in', 'success')


        # TODO: descomentar el código a continuación cuando se tenga
        # la funcionalidad de creación de usuarios implementada en la
        # API
        # Create the user's JSON
        #usuario = {}
        #usuario["email"] = email,
        #usuario["first_name"] = name,
        ##usuario["password"] = password

        #usuario_json = json.dumps(usuario, ensure_ascii=False)

        # Send the JSON to the API REST using the POST method
        #response = requests.post('http://localhost:8080/users', json=usuario_json)

        # Print in the console the response from the API
        #print ('response from server:'),res.text

        return redirect(url_for('login'))

    if (request.method == 'POST'):
        return render_template('register.html', form=form, auth=current_user.is_authenticated)

    return render_template('register.html', form=RegisterForm(), auth=current_user.is_authenticated)

@app.route('/logout')
def logout():
    # TODO: Cuando esté disponible la API se borrará la fila de la tabla de la base de Flask
    # en la que se encuentre la sesión que coincida con la que se va a cerrar, la cual se identificará
    # haciendo uso del token de sesión
    logout_user()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html', auth=current_user.is_authenticated)

@app.route('/blog')
def blog():
    return render_template('blog.html', auth=current_user.is_authenticated)

@app.route('/contact')
def contact():
    return render_template('contact.html', auth=current_user.is_authenticated)

@app.route('/listings')
def listing():
    return render_template('listings.html', auth=current_user.is_authenticated)

@app.route('/venderObjeto')
def venderObjeto():
    return render_template('venderObjeto.html', auth=current_user.is_authenticated)

@app.route("/upload", methods=['POST'])
def upload():
    # Creamos la ruta donde vamos a guardar las imagenes
    target = os.path.join(APP_ROOT, 'static/client_images/')
    print(target)

    # Si no existe la carpeta, la creamos.
    if not os.path.isdir(target):
        os.mkdir(target)

    #Tenemos que hacer un bucle para guardar/enviar todas las imagenes que se quieren subir
    # (El cliente puere queder subir varias)
    for file in request.files.getlist("file"):
        print(file) #Debug
        # Cogemos el nombre del archivo como nombre que se va a guardar, por ahora.
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)  #Debug
        file.save(destination)

    # Redirige a la ruta deseada, se pueden pasar parametros
    return redirect("/single")

# Devuelve las imagenes de un directorio
@app.route('/imagenes/<filename>')
def send_image(filename):
    return send_from_directory("static/client_images", filename)

@app.route('/single')
def get_gallery():
    #Devuelve un vector de nombres de imgenes de la ruta especificada
    image_names = os.listdir('./static/client_images')
    print(image_names)  #Debug
    return render_template("single.html", image_names=image_names, auth=current_user.is_authenticated)

@app.route('/profile')
def profile():
    products = requests.get('https://api.punkapi.com/v2/beers')
    return render_template('profile.html', auth=current_user.is_authenticated, prods=json.loads(products.text))

if __name__ == '__main__':
    app.secret_key = 'secret_key_Selit!_123'
    app.run(debug=True)
