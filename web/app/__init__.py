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
    return render_template('index.html', userauth=current_user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Check if the current user was already loged in
    if current_user.is_authenticated:
        print("Ya estabas logeado como")
        print(current_user.get_username())
        return redirect('/')
    form = LoginForm()
    if form.is_submitted():
        email = form.email.data
        password = form.password.data

        # Get User class of the user that is trying to log in
        usuario = {'email': email, 'password': password}

        # Send the JSON to the API REST using the POST method
        response = requests.post(url='http://35.234.77.87:8080/login', json=usuario, headers={'Authorization': ''})
        
        if response.status_code == 200:
            # Use the token to search in the database so that it is posible to have several sessions of the same user (differentiated by the token)
            user = User.query.filter_by(token=response.headers['Authorization']).first()
            if user is None:
                # If the user does not exist in the database that is used for sessions
                # add him to the database
                user = User(username=form.email.data, user_id=response.headers['idUsuario'], token=response.headers['Authorization'])
                db.session.add(user)
                db.session.commit()
            # Use the User class to login
            # The data from remmember_me is also taken as a parameter as it will define the
            # type of the session
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        else:
            # Authentication failure, go back to the login page
            return redirect('/login')

    return render_template('login.html', title='Log In', form=form, userauth=current_user)


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
        password = form.password.data

        # Create the user's JSON
        usuario = {'email':email, 'first_name':name, 'password':password}
        print(usuario)

        # Send the JSON to the API REST using the POST method
        response = requests.post(url='http://35.234.77.87:8080/users', json=usuario)

        # Print in the console the response from the API
        return redirect(url_for('login'))

    if (request.method == 'POST'):
        return render_template('register.html', form=form, userauth=current_user)

    return render_template('register.html', form=RegisterForm(), userauth=current_user)

@app.route('/logout')
def logout():
    # Delete the session of the user from the database using the token to identify it
    user = User.query.filter_by(token=current_user.token).first()
    if user != None:
        db.session.delete(user)
    logout_user()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html', userauth=current_user)

@app.route('/blog')
def blog():
    return render_template('blog.html', userauth=current_user)

@app.route('/contact')
def contact():
    return render_template('contact.html', userauth=current_user)

@app.route('/listings')
def listing():
    products = requests.get('https://api.punkapi.com/v2/beers')
    return render_template('listings.html', userauth=current_user, prods=json.loads(products.text))

@app.route('/venderObjeto')
def venderObjeto():
    return render_template('venderObjeto.html', userauth=current_user)

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
    return render_template("single.html", image_names=image_names, userauth=current_user)

@app.route('/profile')
def profile():
    products = requests.get('https://api.punkapi.com/v2/beers')
    response = requests.get(url='http://35.234.77.87:8080/users/' + str(current_user.user_id), headers={'Authorization': current_user.token})
    print(response.text)
    return render_template('profile.html', userauth=current_user, prods=json.loads(products.text), user=json.loads(response.text))

if __name__ == '__main__':
    app.secret_key = 'secret_key_Selit!_123'
    app.run(debug=True)
