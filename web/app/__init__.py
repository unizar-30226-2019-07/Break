from flask import Flask, render_template, session, redirect, request, send_from_directory, flash, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from config import Config
from app.forms import LoginForm, RegisterForm, EditProfile, EditEmail, EditPassword, EditLocation, SubirAnuncioForm, ProductSearch
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

# Para poder acceder a herramientas del sistema operativo
import os

# Para hacer hash de las contraseñas
import requests
import json

# Para mostrar mapas con Google Maps Platform
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
app.config.from_object(Config)
# Database used for session management
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

GoogleMaps(app)

from app import models
from app.models import User

# Constante con la dirección del servidor.
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# URL of the API
url = 'http://35.234.77.87:8080'

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
    form = LoginForm(request.form)
    print(form.validate())
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            password = form.password.data

            # Get User class of the user that is trying to log in
            usuario = {'email': email, 'password': password}

            # Send the JSON to the API REST using the POST method
            response = requests.post(url=url + '/login', json=usuario, headers={'Authorization': ''})

            # Status Code management
            # 200: Login successful
            # 401: User exists but it has not been activated
            # 403: Invalid credentials

            if response.status_code == 200:
                # Use the token to search in the database so that it is posible to have several sessions of the same user (differentiated by the token)
                user = User.query.filter_by(token=response.headers['Authorization']).first()
                if user is None:
                    # If the user does not exist in the database that is used for sessions
                    # add him to the database
                    response2 = requests.get(url = url + '/users?email=' + email, headers={'Authorization': response.headers['Authorization']})
                    user = User(username=form.email.data, user_id=json.loads(response2.text)[0]['idUsuario'], token=response.headers['Authorization'])
                    db.session.add(user)
                    db.session.commit()
                # Use the User class to login
                # The data from remmember_me is also taken as a parameter as it will define the
                # type of the session
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            else:
                # Authentication failure, go back to the login page
                #return redirect('/login')
                if response.status_code == 401:
                    notactivated = True
                else:
                    notactivated = False

                if response.status_code == 403:
                    veriferror = True
                else:
                    veriferror = False

                return render_template('login.html', title='Log In', form=LoginForm(), userauth=current_user, notactivated=notactivated, veriferror = veriferror)

        return render_template('login.html', form=form, userauth=current_user)

    return render_template('login.html', title='Log In', form=LoginForm(), userauth=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    print(form.name.errors)
    print("Registro open")
    print(request.method)
    print(form.validate())
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            last_name = form.lastname.data

            # Create the user's JSON
            usuario = {'email': email, 'first_name': name, 'last_name': last_name, 'password': password, 'location': {'lat': 0, 'lng': 0}}
            print(usuario)

            # Send the JSON to the API REST using the POST method
            response = requests.post(url=url + '/users', json=usuario)

            # Print in the console the response from the API
            return redirect(url_for('login'))

        return render_template('register.html', form=form, userauth=current_user)

    return render_template('register.html', form=RegisterForm(), userauth=current_user)


@app.route('/logout')
def logout():
    # Delete the session of the user from the database using the token to identify it
    user = User.query.filter_by(token=current_user.token).first()
    if user is not None:
        logout_user()
        # db.session.delete(user)
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
    form = ProductSearch(request.form)
    # Parametres that will be used in the search are passed using GET
    minprice = request.args.get('minprice')
    maxprice = request.args.get('maxprice')
    minpublished = request.args.get('minpublished')
    maxpublished = request.args.get('maxpublished')
    category = request.args.get('category')
    status = request.args.get('type')
    keywords = request.args.get('keywords')

    # Base address, parametres will be concatenadted here
    products = url + '/products'
    print(products)
    products += "?lat=0"
    products += "&lng=0"
    products += "&distance=500000000"
    if minprice != None and minprice != "":
        products += "&priceFrom=" + minprice
    else:
        minprice = ''
    if maxprice != None and maxprice != "":
        products += "&priceTo=" + maxprice
    else:
        maxprice = ''
    if minpublished != None and minpublished != "":
        products += "&publishedFrom=" + minpublished
    else:
        minpublished = ''
    if maxpublished != None and maxpublished != "":
        products += "&publishedTo=" + maxpublished
    else:
        maxpublished = ''
    if category != None and category != "":
        products += "&category=" + category
    else:
        category = ''
    if status != None and status != "":
        products += "&status=" + type
    else:
        status = ''
    if keywords != None and keywords != "":
        products += "&search=" + keywords
    else:
        keywords = ''

    products = requests.get(products)

    prods = json.loads(products.text)
    mymap = Map(
        identifier="view-side",
        lat=0,
        lng=0,
        fit_markers_to_bounds = True,
        center_on_user_location=True,
        zoom=15,
        markers=[{
             'icon': None,
             'lat': prod['location']['lat'],
             'lng': prod['location']['lng']
          } for prod in prods],
        cluster=True,
        #cluster_imagepath='https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
        cluster_imagepath=url_for('static', filename='images/m'),
        cluster_gridsize=30,
        style="height:300px;margin:0;",
        language="es",
        region="ES"
    )
    return render_template('listings.html', userauth=current_user, prods=prods, map=mymap, form=form, minprice = minprice, maxprice = maxprice, minpublished = minpublished, maxpublished = maxpublished, status = status, keywords = keywords, category = category)


# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


# Para comprobar que las extensiones son correctas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    print(current_user)
    if current_user.is_authenticated:
        form = SubirAnuncioForm(request.form)
        print("subir anuncio open")
        print(request.method)
        print(form.validate())
        if request.method == 'POST':
            if form.validate():
                # Creamos la ruta donde vamos a guardar las imagenes
                target = os.path.join(APP_ROOT, 'static/client_images/')
                print(target)

                # Si no existe la carpeta, la creamos.
                if not os.path.isdir(target):
                    os.mkdir(target)

                # Tenemos que hacer un bucle para guardar/enviar todas las imagenes que se quieren subir
                # (El cliente puere queder subir varias)
                for file in request.files.getlist("images"):

                    if file.filename == '':
                        flash('No selected file')
                        return redirect('subirAnuncio.html')
                    if file and allowed_file(file.filename):
                        productName = form.productName.data
                        productPrice = form.productPrice.data
                        productCategory = form.productCategory.data
                        productDescripcion = form.productDescription.data
                        productCurrency = "EUR"
                        productOwner = current_user.user_id
                        productType = "sale"

                        producto = {'type': productType,
                                'title': productName,
                                'description': productDescripcion,
                                'owner_id': current_user.user_id,
                                'location': {'lat': 0, 'lng': 0},
                                'category': productCategory,
                                'price': productPrice,
                                'currency': productCurrency}

                        print(producto)
                        print(file) # Debug
                        # Cogemos el nombre del archivo como nombre que se va a guardar, por ahora.
                        filename = secure_filename(file.filename)
                        print(filename)

                        #destination = "/".join([target, filename])
                        #print(destination)  # Debug
                        #file.save(destination)

                        response = requests.post(url=url + '/products', json=producto, headers={'Authorization': current_user.token})
                        print(response.text)

                # Redirige a la ruta deseada, se pueden pasar parametros
                return redirect("/")

            return render_template('subirAnuncio.html', form=form, userauth=current_user)

        return render_template('subirAnuncio.html', form=SubirAnuncioForm(), userauth=current_user)
    else:
        return redirect("/login")

# Devuelve las imagenes de un directorio
@app.route('/imagenes/<filename>')
def send_image(filename):
    return send_from_directory("static/client_images", filename)

@app.route('/single/<prod_id>')
def get_gallery(prod_id):
    # Devuelve un vector de nombres de imgenes de la ruta especificada
    image_names = os.listdir(APP_ROOT + '/static/client_images')
    #print(image_names)
    response = requests.get(url + "/products/" + str(prod_id) + "?lng=0&lat=0")
    prod = json.loads(response.text)
    # print(response.text)

    mymap = Map(
        identifier="view-side",
        lat=prod['location']['lat'],
        lng=prod['location']['lng'],
        zoom=15,
        circles=[(prod['location']['lat'], prod['location']['lng'], 200)],
        style="height:400px;margin:0;",
        language="es",
        region="ES"
    )

    return render_template("single.html", image_names=image_names, userauth=current_user, prod=prod, map=mymap)

@app.route('/user/<user_id>')
def user(user_id):
    on_sale = requests.get(url + '/products?lat=0&lng=0&distance=5000000000&owner=' + str(user_id) + '&status=en%20venta')
    sold = requests.get(url + '/products?lat=0&lng=0&distance=5000000000&owner=' + str(user_id) + '&status=vendido')
    response = requests.get(url=url + '/users/' + str(user_id), headers={'Authorization': current_user.token})
    # If there is an error retrieving the user (no permissions) the user will be redirected to the login page
    if response.status_code != 200:
        return redirect("/login")
    else:

        user = json.loads(response.text)

        mymap = Map(
            identifier="view-side",
            lat=user['location']['lat'],
            lng=user['location']['lng'],
            zoom=15,
            circles=[(user['location']['lat'], user['location']['lng'], 200)],
            style="height:200px;margin:0;",
            language="es",
            region="ES"
        )

        return render_template('profile.html', userauth=current_user, on_sale=json.loads(on_sale.text), \
            sold=json.loads(sold.text), wishlist=[], user=user, map=mymap)


@app.route('/profile')
def profile():
    return redirect(url_for('user', user_id=current_user.user_id))

@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    response = requests.get(url=url + '/users/' + str(current_user.user_id), headers={'Authorization': current_user.token})
    user = json.loads(response.text)
    print(user['gender'])
        
    form_location=EditLocation(prefix="location")
    form_password=EditPassword(prefix="password")
    form_email=EditEmail(prefix="email")
    form_profile=EditProfile(prefix="profile")

    # If there is an error retrieving the user (no permissions) the user will be redirected to the login page
    if response.status_code != 200:
        return redirect("/login")
    else:
        if request.method == 'POST':
            form_profile = EditProfile(request.form, prefix="profile")
            form_password = EditPassword(request.form, prefix="password")
            form_email = EditEmail(request.form, prefix="email")
            form_location=EditLocation(request.form, prefix="location")

            if form_profile.submit.data and form_profile.validate_on_submit():
                user['first_name'] = form_profile.name.data
                user['last_name'] = form_profile.lastname.data
                user['gender'] = form_profile.gender.data

                # Send the JSON to the API REST using the POST method
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user, headers={'Authorization': current_user.token})
                return redirect(url_for('profile'))

            elif form_password.submit.data and form_password.validate_on_submit():
                user['password'] = form_password.password.data
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user, headers={'Authorization': current_user.token})
                return redirect(url_for('profile'))

            elif form_email.submit.data and form_email.validate_on_submit():
                user['email'] = form_email.email.data
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user, headers={'Authorization': current_user.token})
                return redirect(url_for('logout'))

            elif form_location.submit.data and form_location.validate_on_submit():
                user['location']['lat'] = form_location.lat.data
                user['location']['lng'] = form_location.lng.data
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user, headers={'Authorization': current_user.token})
                return redirect(url_for('profile'))

        form_profile.gender.default = user['gender']
        form_profile.process()

        return render_template('editprofile.html', form_profile=form_profile, form_email=form_email, \
            form_password=form_password, form_location=form_location, userauth=current_user, user=user, \
            GOOGLEMAPS_KEY=app.config['GOOGLEMAPS_KEY'])

@app.route('/verify')
def verify():
    random= request.args.get('random', default=1, type=str)
    print(random)
    response = requests.post(url=url + '/verify?random=' + str(random))
    print(response.text)
    return redirect("/login")

if __name__ == '__main__':
    app.secret_key = 'secret_key_Selit!_123'
    app.run(debug=True)
