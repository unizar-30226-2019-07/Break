# crea el objeto app como una instancia de la class Flask
from flask import Flask, render_template, session, redirect
from flask_bootstrap import Bootstrap
from config import Config
from app.forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)

Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if 'username' in session:
        username = session['username']
        print("Ya estabas logeado como " + username)
        return redirect('/')
    if form.is_submitted():
        print("Usuario: " + form.username.data)
        print("Contraseña: " + form.password.data)
        session['username'] = form.username.data
        return redirect('/')
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
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

if __name__ == '__main__':
    app.run(debug=True)
