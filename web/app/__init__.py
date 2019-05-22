from flask import Flask, render_template, session, redirect, request, send_from_directory, flash, url_for, jsonify, \
    abort
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from config import Config
from app.forms import LoginForm, RegisterForm, EditProfile, EditEmail, EditPassword, EditLocation, SubirAnuncioForm, \
    ProductSearch, EditPicture, Review, bidPlacementForm, reportForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
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

import urllib, hashlib

app.jinja_env.globals['urllib'] = urllib
app.jinja_env.globals['hashlib'] = hashlib

import base64

from app import models
from app.models import User

# Constante con la dirección del servidor.
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# URL of the API
url = 'https://selit.naval.cat:8443'

app.jinja_env.globals['api'] = url

import datetime
app.jinja_env.globals['now'] = datetime.datetime.utcnow
app.jinja_env.globals['strptime'] = datetime.datetime.strptime

@login.user_loader
def load_user(id):
    # Required function for users to log in
    # Flask_login uses the "id" of the user in the database
    # to manage sessions
    return User.query.get(str(id))


@app.route('/')
def index():
    # Base URLs
    products = url + '/products'
    auctions = url + '/auctions'

    lat = 0
    lng = 0
    args = ""
    if current_user.is_authenticated:
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            if usuario.status_code != 200:
                print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        localizacion = json.loads(usuario.text)['location']
        lng = localizacion['lng']
        lat = localizacion['lat']
        args += "?distance=100"

    else:
        # If the user is not logged in show products from all around the globe
        args += "?distance=1000000000000000"

    args += "&lng=" + str(lng) + "&lat=" + str(lat) + "&$size=3" + "&$page=0" + "&$sort=published DESC"

    products += args
    auctions += args

    products = requests.get(products)
    if app.debug:
        if products.status_code != 200:
            print(products.text)
    else:
        if products.status_code != 200:
            abort(products.status_code)
    prods = json.loads(products.text)

    auctions = requests.get(auctions)
    if app.debug:
        if auctions.status_code != 200:
            print(auctions.text)
    else:
        if auctions.status_code != 200:
            abort(auctions.status_code)
    auctions = json.loads(auctions.text)

    return render_template('index.html', userauth=current_user, auctions=auctions, prods=prods)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the current user was already loged in
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm(request.form)

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
                user = User.query.filter_by(id=response.headers['Authorization']).first()
                if user is None:
                    # If the user does not exist in the database that is used for sessions
                    # add him to the database
                    response2 = requests.get(url=url + '/users?email=' + email,
                                             headers={'Authorization': response.headers['Authorization']})
                    if app.debug:
                        if response2.status_code != 200:
                            print(response2.text)
                    else:
                        if response2.status_code != 200:
                            abort(response2.status_code)
                    user = User(id=response.headers['Authorization'], username=form.email.data,
                                user_id=json.loads(response2.text)[0]['idUsuario'])
                    db.session.add(user)
                    db.session.commit()
                # Use the User class to login
                # The data from remmember_me is also taken as a parameter as it will define the
                # type of the session
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            else:
                # Authentication failure, go back to the login page
                # return redirect('/login')
                if response.status_code == 401:
                    notactivated = True
                else:
                    notactivated = False

                if response.status_code == 403:
                    veriferror = True
                else:
                    veriferror = False

                return render_template('login.html', title='Log In', form=LoginForm(), userauth=current_user,
                                       notactivated=notactivated, veriferror=veriferror)

        return render_template('login.html', form=form, userauth=current_user)

    return render_template('login.html', title='Log In', form=LoginForm(), userauth=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            last_name = form.lastname.data

            # Create the user's JSON
            usuario = {'email': email, 'first_name': name, 'last_name': last_name, 'password': password,
                       'location': {'lat': 0, 'lng': 0}}

            # Send the JSON to the API REST using the POST method
            response = requests.post(url=url + '/users', json=usuario)

            # Print in the console the response from the API
            return redirect(url_for('login'))

        return render_template('register.html', form=form, userauth=current_user)

    return render_template('register.html', form=RegisterForm(), userauth=current_user)


@app.route('/logout')
def logout():
    # Delete the session of the user from the database using the token to identify it
    user = User.query.filter_by(id=current_user.id).first()
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


@app.route('/auctions')
def auctions():
    # Value is 1 whenever the user is on the first/last page
    firstpage = 0
    lastpage = 0
    # Value is 1 when the user has entered an invalid min or max price
    errormin = 0
    errormax = 0
    errordist = 0

    # Base address, parametres will be concatenadted here
    products = url + '/auctions'

    lat = 0
    lng = 0
    if current_user.is_authenticated:
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            if usuario.status_code != 200:
                print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        localizacion = json.loads(usuario.text)['location']
        lng = localizacion['lng']
        lat = localizacion['lat']

    form = ProductSearch(request.form)
    # Parametres that will be used in the search are passed using GET
    page = request.args.get('page')
    size = request.args.get('resultados')
    minprice = request.args.get('minprice')
    maxprice = request.args.get('maxprice')
    minpublished = request.args.get('minpublished')
    maxpublished = request.args.get('maxpublished')
    category = request.args.get('category')
    status = request.args.get('estado')
    keywords = request.args.get('keywords')
    ordenacion = request.args.get('ordenacion')
    distancia = request.args.get('distancia')

    products += "?lat=" + str(lat)
    products += "&lng=" + str(lng)
    if minprice != None and minprice != "":
        if not minprice.isdigit():
            errormin = 1
        else:
            # The minprice will not be added to the query if it has
            # been entered incorrectly
            products += "&priceFrom=" + minprice
    else:
        minprice = ''
    if maxprice != None and maxprice != "":
        if not maxprice.isdigit():
            errormax = 1
        else:
            # The minprice will not be added to the query if it has
            # been entered incorrectly
            products += "&priceTo=" + maxprice
    else:
        maxprice = ''

    if distancia != None and distancia != "":
        if not distancia.isdigit():
            errordist = 1;
            products += "&distance=500000000"
        else:
            products += "&distance=" + distancia
    else:
        products += "&distance=500000000"
        distancia = ''

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
        products += "&status=" + status
    else:
        status = ''
    if keywords != None and keywords != "":
        products += "&search=" + keywords
    else:
        keywords = ''
    if ordenacion != None and ordenacion != "":
        products += "&$sort=" + ordenacion
    else:
        ordenacion = ''
    if size != None and size != "":
        products += "&$size=" + size
    else:
        # When the number of products per page is not specified it
        # will be set to 15
        size = 15
        products += "&$size=15"

    if page != None and page != "":
        page = int(page)
        productsNext = products + "&$page=" + str(page + 1)
        products += "&$page=" + str(page)
    else:
        # Page defaults to 0 when no page is specified
        # Then the next page is the second one
        productsNext = products + "&$page=1"
        products += "&$page=0"
        page = 0

    if page == 0:
        firstpage = 1

    if current_user.is_authenticated:
        products = requests.get(products + '&token=yes', headers={'Authorization': current_user.id})
    else:
        products = requests.get(products)
    if app.debug:
        if products.status_code != 200:
            print(products.text)
    else:
        if products.status_code != 200:
            abort(products.status_code)
    prods = json.loads(products.text)
    # When there are no results in the next page we are showing the last page"
    if len(json.loads(requests.get(productsNext).text)) == 0:
        lastpage = 1
    # Generate addresses for the previous/next page buttons# Generate addresses for the previous/next page buttons# Generate addresses for the previous/next page buttons
    nextPageAddr = "/auctions" + ("?minprice=" + minprice) * (not errormin) + ("&maxprice=" + maxprice) * (
        not errormax) + "&minpublished=" + minpublished + "&maxpublished=" + maxpublished + "&category=" + category + "&keywords=" + keywords + "&resultados=" + str(
        size) + "&ordenacion=" + ordenacion + "&page=" + str(page + 1) + "&status=" + status
    prevPageAddr = "/auctions" + ("?minprice=" + minprice) * (not errormin) + ("&maxprice=" + maxprice) * (
        not errormax) + "&minpublished=" + minpublished + "&maxpublished=" + maxpublished + "&category=" + category + "&keywords=" + keywords + "&resultados=" + str(
        size) + "&ordenacion=" + ordenacion + "&page=" + str(page - 1) + "&status=" + status

    mymap = Map(
        identifier="view-side",
        lat=lat,
        lng=lng,
        fit_markers_to_bounds=True,
        center_on_user_location=True,
        zoom=15,
        markers=[{
            'icon': None,
            'lat': prod['location']['lat'],
            'lng': prod['location']['lng']
        } for prod in prods],
        cluster=True,
        # cluster_imagepath='https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
        cluster_imagepath=url_for('static', filename='images/m'),
        cluster_gridsize=30,
        style="height:300px;margin:0;",
        language="es",
        region="ES"
    )
    return render_template('listings.html', userauth=current_user, prods=prods, map=mymap, form=form, minprice=minprice,
                           maxprice=maxprice, minpublished=minpublished, maxpublished=maxpublished, status=status,
                           keywords=keywords, category=category, next=nextPageAddr, prev=prevPageAddr, first=firstpage,
                           last=lastpage, sort=ordenacion, errormin=errormin, errormax=errormax, resultados=size,
                           auction=True, distancia=distancia, errordist=errordist)


@app.route('/listings')
def listing():
    # Value is 1 whenever the user is on the first/last page
    firstpage = 0
    lastpage = 0
    # Value is 1 when the user has entered an invalid min or max price
    errormin = 0
    errormax = 0
    errordist = 0

    # Base address, parametres will be concatenadted here
    products = url + '/products'

    lat = 0
    lng = 0
    if current_user.is_authenticated:
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            if usuario.status_code != 200:
                print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        localizacion = json.loads(usuario.text)['location']
        lng = localizacion['lng']
        lat = localizacion['lat']

    products += "?lat=" + str(lat)
    products += "&lng=" + str(lng)

    form = ProductSearch(request.form)
    # Parametres that will be used in the search are passed using GET
    page = request.args.get('page')
    size = request.args.get('resultados')
    minprice = request.args.get('minprice')
    maxprice = request.args.get('maxprice')
    minpublished = request.args.get('minpublished')
    maxpublished = request.args.get('maxpublished')
    category = request.args.get('category')
    status = request.args.get('estado')
    keywords = request.args.get('keywords')
    ordenacion = request.args.get('ordenacion')
    distancia = request.args.get('distancia')

    if minprice != None and minprice != "":
        if not minprice.isdigit():
            errormin = 1
        else:
            # The minprice will not be added to the query if it has
            # been entered incorrectly
            products += "&priceFrom=" + minprice
    else:
        minprice = ''
    if maxprice != None and maxprice != "":
        if not maxprice.isdigit():
            errormax = 1
        else:
            # The minprice will not be added to the query if it has
            # been entered incorrectly
            products += "&priceTo=" + maxprice
    else:
        maxprice = ''

    if distancia != None and distancia != "":
        if not distancia.isdigit():
            errordist = 1;
            products += "&distance=500000000"
        else:
            products += "&distance=" + distancia
            distancia = ''
    else:
        products += "&distance=500000000"
        distancia = ''

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
        products += "&status=" + status
    else:
        status = ''
    if keywords != None and keywords != "":
        products += "&search=" + keywords
    else:
        keywords = ''
    if ordenacion != None and ordenacion != "":
        products += "&$sort=" + ordenacion
    else:
        ordenacion = ''
    if size != None and size != "":
        products += "&$size=" + size
    else:
        # When the number of products per page is not specified it
        # will be set to 15
        size = 15
        products += "&$size=15"

    if page != None and page != "":
        page = int(page)
        productsNext = products + "&$page=" + str(page + 1)
        products += "&$page=" + str(page)
    else:
        # Page defaults to 0 when no page is specified
        # Then the next page is the second one
        productsNext = products + "&$page=1"
        products += "&$page=0"
        page = 0

    if page == 0:
        firstpage = 1

    if current_user.is_authenticated:
        products = requests.get(products + "&token=yes", headers={'Authorization': current_user.id})
    else:
        products = requests.get(products)
    if app.debug:
        if products.status_code != 200:
            print(products.text)
    else:
        if products.status_code != 200:
            abort(products.status_code)
    prods = json.loads(products.text)
    # When there are no results in the next page we are showing the last page"
    if len(json.loads(requests.get(productsNext).text)) == 0:
        lastpage = 1
    # Generate addresses for the previous/next page buttons# Generate addresses for the previous/next page buttons# Generate addresses for the previous/next page buttons
    nextPageAddr = "/listings" + ("?minprice=" + minprice) * (not errormin) + ("&maxprice=" + maxprice) * (
        not errormax) + "&minpublished=" + minpublished + "&maxpublished=" + maxpublished + "&category=" + category + "&keywords=" + keywords + "&resultados=" + str(
        size) + "&ordenacion=" + ordenacion + "&page=" + str(page + 1) + "&status=" + status
    prevPageAddr = "/listings" + ("?minprice=" + minprice) * (not errormin) + ("&maxprice=" + maxprice) * (
        not errormax) + "&minpublished=" + minpublished + "&maxpublished=" + maxpublished + "&category=" + category + "&keywords=" + keywords + "&resultados=" + str(
        size) + "&ordenacion=" + ordenacion + "&page=" + str(page - 1) + "&status=" + status

    mymap = Map(
        identifier="view-side",
        lat=lat,
        lng=lng,
        fit_markers_to_bounds=True,
        center_on_user_location=True,
        zoom=15,
        markers=[{
            'icon': None,
            'lat': prod['location']['lat'],
            'lng': prod['location']['lng']
        } for prod in prods],
        cluster=True,
        # cluster_imagepath='https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
        cluster_imagepath=url_for('static', filename='images/m'),
        cluster_gridsize=30,
        style="height:300px;margin:0;",
        language="es",
        region="ES"
    )
    return render_template('listings.html', userauth=current_user, prods=prods, map=mymap, form=form, minprice=minprice,
                           maxprice=maxprice, minpublished=minpublished, maxpublished=maxpublished, status=status,
                           keywords=keywords, category=category, next=nextPageAddr, prev=prevPageAddr, first=firstpage,
                           last=lastpage, sort=ordenacion, errormin=errormin, errormax=errormax, resultados=size,
                           auction=0, distancia=distancia, errordist=errordist)


# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


# Para comprobar que las extensiones son correctas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return editproduct(0)


@app.route("/uploadAuction", methods=['GET', 'POST'])
def uploadAuction():
    return editauction(0)


@app.route("/single/<prod_id>/delete", methods=['GET'])
def deleteproduct(prod_id):
    isAuction = int(request.args.get('isAuction') or '0') == 1
    if int(isAuction) == 1:
        response = requests.delete(url=url + '/auctions/' + prod_id, headers={'Authorization': current_user.id})
    else:
        response = requests.delete(url=url + '/products/' + prod_id, headers={'Authorization': current_user.id})
    return redirect(url_for('profile'))


@app.route("/single/<prod_id>/edit", methods=['GET', 'POST'])
def editproduct(prod_id):
    isAuction = int(request.args.get('isAuction') or '0') == 1
    isNew = 0
    lat = 0
    lng = 0
    noDateError = 0
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            if usuario.status_code != 200:
                print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        localizacion = json.loads(usuario.text)['location']
        lng = localizacion['lng']
        lat = localizacion['lat']

    if int(prod_id) > 0:
        # Editar producto preexistente
        if isAuction:
            response = requests.get(url + "/auctions/" + str(prod_id) + "?lng=" + str(lng) + "&lat=" + str(lat))
        else:
            response = requests.get(url + "/products/" + str(prod_id) + "?lng=" + str(lng) + "&lat=" + str(lat))
        if app.debug:
            if response.status_code != 200:
                print(response.text)
        else:
            if response.status_code != 200:
                abort(response.status_code)
        product = json.loads(response.text)
    else:
        isAuction = False
        isNew = 1
        # Crear producto nuevo
        product = { 'title': '',
            'description': '',
            'owner_id': current_user.user_id,
            'location': {
                'lat': lat, 
                'lng': lng
            },
            'category': '',
            'currency': 'EUR',
            'media': []
        }

    form_sale = SubirAnuncioForm(prefix="sale")
    if request.method == 'POST':
        form_sale = SubirAnuncioForm(request.form, prefix="sale")
        if form_sale.submit.data and form_sale.validate_on_submit():
            print("A")

            # Tenemos que hacer un bucle para guardar/enviar todas las imagenes que se quieren subir
            # (El cliente puere queder subir varias)
            mime = request.form.getlist("mime[]")
            base64 = request.form.getlist("base64[]")
            product['media'] = []
            for i, idImagen in enumerate(request.form.getlist("idImagen[]")):
                if (int(idImagen) > 0):
                    product['media'].append({
                        'idImagen': idImagen,
                        'base64': None,
                        'mime': None,
                        'charset': None
                    })
                else:
                    product['media'].append({
                        'base64': base64[i],
                        'mime': mime[i],
                        'charset': 'utf-8'
                    })
            if int(prod_id) == 0:
                isAuction = False
                if request.form.getlist('isAuction') != []:
                    isAuction = (request.form.getlist('isAuction')[0] == 'y')
            product['title'] = form_sale.name.data
            product['description'] = form_sale.description.data
            product['location']['lat'] = form_sale.lat.data
            product['location']['lng'] = form_sale.lng.data
            product['category'] = form_sale.category.data
            if not isAuction:
                product['price'] = float(form_sale.price.data)
                print(product['price'])
            else:
                product['startPrice'] = float(form_sale.price.data)
                product['endDate'] = str(form_sale.enddate.data) 
                product['type'] = "sale"

            if int(prod_id) > 0:
                if int(isAuction) == 1:
                    if product['endDate']  != None:
                        product['owner_id'] = current_user.user_id
                        response = requests.put(url=url + '/auctions/' + prod_id, json=product,
                                            headers={'Authorization': current_user.id})
                        if app.debug:
                            if response.status_code != 200:
                                print(response.text)
                        else:
                            if response.status_code != 200:
                                abort(500)
                    else:
                        noDateError = 1;
                else:
                    response = requests.put(url=url + '/products/' + prod_id, json=product,
                                        headers={'Authorization': current_user.id})
                    print(response.text)
                    if app.debug:
                        if response.status_code != 200:
                            print(response.text)
                    else:
                        if response.status_code != 200:
                            abort(500)

            else:
                if isAuction:
                    print(len(str(product['endDate'])))
                    if len(str(product['endDate'])) != 4:
                        response = requests.post(url=url + '/auctions', json=product, headers={'Authorization': current_user.id})
                    else:
                        noDateError = 1;
                else:
                    response = requests.post(url=url + '/products', json=product, headers={'Authorization': current_user.id})

            if noDateError == 0:
                # Redirige a la ruta deseada, se pueden pasar parametros
                return redirect(url_for('profile'))

    form_sale.category.default = product['category']
    form_sale.description.default = product['description']
    form_sale.process()

    return render_template('subirAnuncio.html', form_sale=form_sale, userauth=current_user, product=product, isAuction=(int(isAuction) == 1), isNew=(prod_id == 0), noDateError=(int(noDateError==1)))

# Devuelve las imagenes de un directorio
@app.route('/imagenes/<filename>')
def send_image(filename):
    return send_from_directory("static/client_images", filename)


@app.route('/single/<prod_id>')
def get_gallery(prod_id):
    lat = 0
    lng = 0
    if current_user.is_authenticated:
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        localizacion = json.loads(usuario.text)['location']
        lng = localizacion['lng']
        lat = localizacion['lat']

    if current_user.is_authenticated:
        response = requests.get(
            url + "/products/" + str(prod_id) + "?lng=" + str(lng) + "&lat=" + str(lat) + "&token=yes",
            headers={'Authorization': current_user.id})
    else:
        response = requests.get(url + "/products/" + str(prod_id) + "?lng=" + str(lng) + "&lat=" + str(lat))
    if app.debug:
        if response.status_code != 200:
            print(response.text)
    else:
        if response.status_code != 200 and not app.debug:
            abort(response.status_code)
    prod = json.loads(response.text)

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
    return render_template("single.html", userauth=current_user, prod=prod, map=mymap, auction=False)

def review(prod_id, isAuction):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            if usuario.status_code != 200:
                print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        
        usuario = json.loads(usuario.text)

    if isAuction:
        response = requests.get(url + "/auctions/" + str(prod_id) + "?lng=0&lat=0")
    else:
        response = requests.get(url + "/products/" + str(prod_id) + "?lng=0&lat=0")
    if app.debug:
        if response.status_code != 200:
            print(response.text)
    else:
        if response.status_code != 200 and not app.debug:
            abort(response.status_code)
    prod = json.loads(response.text)

    form_review = Review(prefix="review")
    if request.method == 'POST':
        form_review = Review(request.form, prefix="review")
        if form_review.submit.data and form_review.validate_on_submit():

            review = {}
            review['id_comprador'] = usuario['idUsuario']
            review['id_anunciante'] = prod['owner']['idUsuario']
            review['valor'] = form_review.stars.data
            review['comentario'] = form_review.comment.data
            if isAuction:
                review['id_subasta'] = prod_id
            else:
                review['id_producto'] = prod_id

            response = requests.post(url=url + '/users/' + str(review['id_anunciante']) + '/reviews', json=review,
                                    headers={'Authorization': current_user.id})
            if app.debug:
                if response.status_code != 200:
                    print(response.text)
            else:
                if response.status_code != 200:
                    abort(response.status_code)

            if isAuction:
                return redirect(url_for('get_auction', prod_id=prod_id))
            else:
                return redirect(url_for('get_gallery', prod_id=prod_id))

    return render_template('review.html', form_review=form_review, userauth=current_user)

@app.route('/single/<prod_id>/review', methods=['GET', 'POST'])
def review_gallery(prod_id):
    return review(prod_id, False)

@app.route('/auction/<prod_id>', methods=['GET', 'POST'])
def get_auction(prod_id):
    lat = 0
    lng = 0
    errorNum = 0
    errorNoLogin = 0
    winnerId = - 1
    finSub = 0
    if current_user.is_authenticated:
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            if usuario.status_code != 200:
                print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        localizacion = json.loads(usuario.text)['location']
        lng = localizacion['lng']
        lat = localizacion['lat']

    response_sell = requests.put(url + "/auctions/" + str(prod_id) + "/sell")
    if len(response_sell.text) > 0:
        if json.loads(response_sell.text)['amount'] > 0:
            winnerId = int(json.loads(response_sell.text)['bidder']['idUsuario'])
        finSub = 1
    if current_user.is_authenticated:
        response = requests.get(url + "/auctions/" + str(prod_id) + "?lng=" + str(lng) + "&lat=" + str(lat) + "&token=yes", headers={'Authorization': current_user.id})
    else:
        response = requests.get(url + "/auctions/" + str(prod_id) + "?lng=" + str(lng) + "&lat=" + str(lat))

    print(response_sell.text)
    if app.debug:
        if response.status_code != 200:
            print(response.text)
    else:
        if response.status_code != 200:
            abort(response.status_code)
    prod = json.loads(response.text)
    print(response.text)
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

    form = bidPlacementForm(request.form)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            errorNoLogin = 1
        else:
            amount = form.amount.data
            if not str(amount).replace('.','',1).isdigit():
                errorNum = 1
            else: 
                if prod['lastBid'] == None:
                    if int(prod['startPrice']) >= float(amount):
                        errorNum = 1
                else:
                    if int(prod['lastBid']['amount']) >= float(amount):
                        errorNum = 1
        if errorNoLogin == 0 and errorNum == 0:
            puja = {'amount': amount, 'bidder_id': current_user.user_id}
            response = requests.post(url=url + '/auctions/' + str(prod_id) + '/bid', json=puja, headers={'Authorization': current_user.id})
            # Reload the product to update the price
            response = requests.get(url + "/auctions/" + str(prod_id) + "?lng=" + str(lng) + "&lat=" + str(lat) + "&token=yes", headers={'Authorization': current_user.id})
            prod = json.loads(response.text)

    return render_template("single.html", userauth=current_user, prod=prod, map=mymap, auction=True, form=form, errorNum=errorNum, errorNoLogin=errorNoLogin, winnerId=int(winnerId), finSub=int(finSub))

@app.route('/auction/<prod_id>/review', methods=['GET', 'POST'])
def review_auction(prod_id):
    return review(prod_id, True)

@app.route('/user/<user_id>')
def user(user_id):
    lat = 0
    lng = 0
    token = "no"
    headers = {}
    if current_user.is_authenticated:
        token = "yes"
        headers = {'Authorization': current_user.id}
        usuario = requests.get(url=url + '/users/' + str(current_user.user_id),
                               headers={'Authorization': current_user.id})
        if app.debug:
            if usuario.status_code != 200:
                print(usuario.text)
        else:
            if usuario.status_code != 200:
                abort(usuario.status_code)
        localizacion = json.loads(usuario.text)['location']
        lng = localizacion['lng']
        lat = localizacion['lat']
    else:
        lng = 0
        lat = 0

    ###############################
    ####    NORMAL PRODUCTS    ####
    ###############################

    on_sale = requests.get(url + '/products?lat=' + str(lat) + '&lng=' + str(lng) + '&distance=5000000000&owner=' + str(
        user_id) + '&status=en%20venta&token=' + token, headers=headers)
    if app.debug:
        if on_sale.status_code != 200:
            print(on_sale.text)
    else:
        if on_sale.status_code != 200:
            abort(on_sale.status_code)
    products_on_sale = json.loads(on_sale.text)

    sold = requests.get(url + '/products?lat=' + str(lat) + '&lng=' + str(lng) + '&distance=5000000000&owner=' + str(
        user_id) + '&status=vendido&token=' + token, headers=headers)
    if app.debug:
        if sold.status_code != 200:
            print(sold.text)
    else:
        if sold.status_code != 200:
            abort(sold.status_code)
    products_sold = json.loads(sold.text)

    if current_user.is_authenticated and str(current_user.user_id) == user_id:
        wishlist = requests.get(url + '/users/' + str(user_id) + '/wishes_products?lat=' + str(lat) + '&lng=' + str(
            lng) + '&distance=5000000000&token=' + token, headers=headers)
        if app.debug:
            if wishlist.status_code != 200:
                print(wishlist.text)
        else:
            if wishlist.status_code != 200:
                abort(wishlist.status_code)
        products_wishlist = json.loads(wishlist.text)
    else:
        products_wishlist = []

    ################################
    ####    AUCTION PRODUCTS    ####
    ################################

    on_sale = requests.get(url + '/auctions?lat=' + str(lat) + '&lng=' + str(lng) + '&distance=5000000000&owner=' + str(
        user_id) + '&status=en%20venta&token=' + token, headers=headers)
    if app.debug:
        if on_sale.status_code != 200:
            print(on_sale.text)
    else:
        if on_sale.status_code != 200:
            abort(on_sale.status_code)
    auctions_on_sale = json.loads(on_sale.text)

    sold = requests.get(url + '/auctions?lat=' + str(lat) + '&lng=' + str(lng) + '&distance=5000000000&owner=' + str(
        user_id) + '&status=vendido&token=' + token, headers=headers)
    if app.debug:
        if sold.status_code != 200:
            print(sold.text)
    else:
        if sold.status_code != 200:
            abort(sold.status_code)
    auctions_sold = json.loads(sold.text)

    if current_user.is_authenticated and str(current_user.user_id) == user_id:
        wishlist = requests.get(url + '/users/' + str(user_id) + '/wishes_auctions?lat=' + str(lat) + '&lng=' + str(
            lng) + '&distance=5000000000&token=' + token, headers=headers)
        if app.debug:
            if wishlist.status_code != 200:
                print(wishlist.text)
        else:
            if wishlist.status_code != 200:
                abort(wishlist.status_code)
        auctions_wishlist = json.loads(wishlist.text)
    else:
        auctions_wishlist = []

    response = requests.get(url=url + '/users/' + str(user_id), headers=headers)
    print(response.text)
    if response.status_code == 403:
        return redirect('/login')
    if app.debug:
        if response.status_code != 200:
            print(response.text)
    else:
        if response.status_code != 200:
            abort(response.status_code)

    reviews = requests.get(url + '/users/' + user_id + '/reviews', headers=headers)
    if app.debug:
        if reviews.status_code != 200:
            print(reviews.text)
    else:
        if reviews.status_code != 200:
            abort(reviews.status_code)

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

    on_sale = products_on_sale + auctions_on_sale
    sold = products_sold + auctions_sold
    wishlist = products_wishlist + auctions_wishlist
    reviews = json.loads(reviews.text);

    return render_template('profile.html', userauth=current_user, on_sale=on_sale, \
                           sold=sold, wishlist=wishlist, user=user, map=mymap, \
                           reviews=reviews)


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return redirect(url_for('user', user_id=current_user.user_id))
    else:
        return redirect(url_for('login'))


@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    response = requests.get(url=url + '/users/' + str(current_user.user_id), headers={'Authorization': current_user.id})
    if app.debug:
        if response.status_code != 200:
            print(response.text)
    else:
        if response.status_code != 200:
            abort(response.status_code)
    user = json.loads(response.text)

    user['picture'] = {'idImagen': user['picture']['idImagen']}

    form_location = EditLocation(prefix="location")
    form_password = EditPassword(prefix="password")
    form_email = EditEmail(prefix="email")
    form_profile = EditProfile(prefix="profile")
    form_picture = EditPicture(prefix="picture")

    # If there is an error retrieving the user (no permissions) the user will be redirected to the login page
    if response.status_code != 200:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form_profile = EditProfile(request.form, prefix="profile")
            form_password = EditPassword(request.form, prefix="password")
            form_email = EditEmail(request.form, prefix="email")
            form_location = EditLocation(request.form, prefix="location")

            if form_profile.submit.data and form_profile.validate_on_submit():
                user['first_name'] = form_profile.name.data
                user['last_name'] = form_profile.lastname.data
                user['gender'] = form_profile.gender.data

                # Send the JSON to the API REST using the POST method
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user,
                                        headers={'Authorization': current_user.id})
                return redirect(url_for('profile'))

            elif form_password.submit.data and form_password.validate_on_submit():
                user['password'] = form_password.password.data
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user,
                                        headers={'Authorization': current_user.id})
                return redirect(url_for('profile'))

            elif form_email.submit.data and form_email.validate_on_submit():
                user['email'] = form_email.email.data
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user,
                                        headers={'Authorization': current_user.id})
                return redirect(url_for('logout'))

            elif form_location.submit.data and form_location.validate_on_submit():
                user['location']['lat'] = form_location.lat.data
                user['location']['lng'] = form_location.lng.data
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user,
                                        headers={'Authorization': current_user.id})

                return redirect(url_for('profile'))
            elif form_picture.submit.data and form_picture.validate_on_submit():
                file = request.files[form_picture.picture.name]
                base64_data = base64.b64encode(file.read())
                user['picture'] = {'mime': file.content_type, 'charset': 'utf-8',
                                   'base64': str(base64_data.decode('utf-8'))}
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user,
                                        headers={'Authorization': current_user.id})
                return redirect(url_for('profile'))
            elif form_picture.delete.data and form_picture.validate_on_submit():
                user['picture'] = {'idImagen': None, 'mime': None, 'charset': None, 'base64': None}
                response = requests.put(url=url + '/users/' + str(current_user.user_id), json=user,
                                        headers={'Authorization': current_user.id})
                return redirect(url_for('profile'))

        form_profile.gender.default = user['gender']
        form_profile.process()

        return render_template('editprofile.html', form_profile=form_profile, form_email=form_email, \
                               form_password=form_password, form_location=form_location, form_picture=form_picture, \
                               userauth=current_user, user=user, GOOGLEMAPS_KEY=app.config['GOOGLEMAPS_KEY'])


@app.route('/verify')
def verify():
    random = request.args.get('random', default=1, type=str)
    response = requests.post(url=url + '/verify?random=' + str(random))
    return redirect(url_for('login'))


@app.route('/chat')
def chat():
    if current_user.is_authenticated:
        response = requests.get(url=url + '/users/' + str(User.get_userid(current_user)),
                                headers={'Authorization': current_user.id})
        if app.debug:
            if response.status_code != 200:
                print(response.text)
        else:
            if response.status_code != 200:
                abort(response.status_code)
        # If there is an error retrieving the user (no permissions) the user will be redirected to the login page
        if response.status_code != 200:
            return redirect(url_for('login'))
        else:
            user = json.loads(response.text)

        return render_template("chatpage.html", userauth=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/report/<user_id>', methods=['GET', 'POST'])
def report(user_id):
    form = reportForm(request.form)
    if request.method == 'POST':
        if form.validate():
            category = form.category.data
            description = form.description.data
            fecha = datetime.datetime.now().strftime('%Y-%m-%d')
            # Create the report's JSON
            informe = {'id_evaluado': user_id, 'id_informador': current_user.user_id, 'descripcion': description, 'fecha_realizacion': fecha,
                       'asunto': category}

            # Send the JSON to the API REST using the PUT method
            response = requests.post(url=url + '/reports/' + str(user_id) + '/report', json=informe, headers={'Authorization': current_user.id})

            print(response.text)
            return redirect('/')

        return render_template('report.html', form=form, userauth=current_user)

    return render_template('report.html', form=reportForm(), userauth=current_user)

@app.route('/reports')
def reports():
    response = requests.get(url=url + '/reports', headers={'Authorization': current_user.id})
    print(response.text)
    return render_template('reports.html', userauth=current_user, reports=json.loads(response.text))

@app.route('/solveReport/<user_id>')
def solveReport(user_id):
    response = requests.get(url=url + '/reports', headers={'Authorization': current_user.id})
    reports = json.loads(response.text)
    i = 0
    report = {}
    while i < len(reports):
        if int(reports[i]["evaluado"]["idUsuario"]) == int(user_id):
            report = reports[i]
        i += 1
    if int(report["evaluado"]['idUsuario']) == int(user_id):
        report['estado_informe'] = "resuelto"
        reportAct = {
                'id_evaluado': report['evaluado']['idUsuario'],
                'id_informador': report['informador']['idUsuario'],
                'descripcion': report['descripcion'],
                'fecha_realizacion': report['fecha_realizacion'],
                'asunto': report['asunto'],
                'estado_informe': "resuelto"}

        response = requests.put(url=url + '/reports/' + str(user_id) + "/report", json=reportAct, headers={'Authorization': current_user.id})
    return redirect('/reports')


@app.route('/firebase-messaging-sw.js')
def firebase_sw():
    return send_from_directory("static/js", 'firebase-messaging-sw.js')


@app.route('/ajax/wishes_products/<prod_id>', methods=['PUT', 'DELETE'])
def wishes_products(prod_id):
    if not current_user.is_authenticated:
        return "", 401

    if request.method == 'PUT':
        response = requests.put(url=url + '/users/' + str(current_user.user_id) + '/wishes_products/' + prod_id,
                                headers={'Authorization': current_user.id})
    elif request.method == 'DELETE':
        response = requests.delete(url=url + '/users/' + str(current_user.user_id) + '/wishes_products/' + prod_id,
                                   headers={'Authorization': current_user.id})

    if app.debug:
        if response.status_code != 200:
            print(response.text)
    return "", response.status_code

@app.route('/ajax/wishes_auctions/<prod_id>', methods=['PUT', 'DELETE'])
def wishes_auctions(prod_id):
    if not current_user.is_authenticated:
        return "", 401

    if request.method == 'PUT':
        response = requests.put(url=url + '/users/' + str(current_user.user_id) + '/wishes_auctions/' + prod_id,
                                headers={'Authorization': current_user.id})
    elif request.method == 'DELETE':
        response = requests.delete(url=url + '/users/' + str(current_user.user_id) + '/wishes_auctions/' + prod_id,
                                   headers={'Authorization': current_user.id})

    if app.debug:
        if response.status_code != 200:
            print(response.text)
    return "", response.status_code


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="404", msg="No encontrado", userauth=current_user), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="500", msg="Error interno", userauth=current_user), 500


if __name__ == '__main__':
    app.secret_key = 'secret_key_Selit!_123'
    app.run(debug=True)
