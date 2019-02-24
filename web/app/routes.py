from flask import render_template, flash, redirect, session
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if 'username' in session:
        username = session['username']
        print("Ya estabas logeado como " + username)
    if form.is_submitted():
        print("Usuario: " + form.username.data)
        print("Contraseña: " + form.password.data)
        session['username'] = form.username.data
        return redirect('/index')
    return render_template('login.html', title='Log In', form=form)
