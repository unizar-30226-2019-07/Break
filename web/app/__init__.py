from flask import Flask, render_template, session, redirect
import requests
import json
from flask_bootstrap import Bootstrap
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

Bootstrap(app)

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

@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/venderObjeto')
def venderObjeto():
    return render_template('venderObjeto.html')

@app.route('/pruebas')
def pruebas():
    posts = requests.get('https://gist.githubusercontent.com/torvic98/50769ae4fa82c8db60e16cedbaf6a5e3/raw/4054f4650f49e8a20f65eea93f4829f2ae41af0a/item.json')
    print(json.loads(posts.text)['title'])
    return render_template('pruebas.html', posts=json.loads(posts.text))

if __name__ == '__main__':
    app.run(debug=True)
