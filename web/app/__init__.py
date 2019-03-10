# Para poder acceder a herramientas del sistema operativo
import os

from flask import Flask, render_template, session, redirect, request, send_from_directory
# from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, logout_user
from config import Config
from app.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

# Bootstrap(app)

@login.user_loader
def load_user(id):
    # Required function for users to log in
    # Flask_login uses the "id" of the user in the database
    # to manage sessions
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Check if the current user was already loged in
    if current_user.is_authenticated:
        print("Ya estabas logeado como")
        return redirect('/')
    form = LoginForm()
    if form.is_submitted():
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
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/listings')
def listing():
    return render_template('listings.html')

@app.route('/venderObjeto')
def venderObjeto():
    return render_template('venderObjeto.html')


@app.route("/upload", methods=['POST'])
def upload():
    # Creamos la ruta donde vamos a guardar las imagenes
    target = os.path.join(APP_ROOT, 'static/client_images/')
    print(target)

    # Si no existe la carpeta, la creamos.
    if not os.path.isdir(target):
        os.mkdir(target)

    #T enemos que hacer un bucle para guardar/enviar todas las imagenes que se quieren subir
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
    return render_template("single.html", image_names=image_names)


if __name__ == '__main__':
    app.run(debug=True)
