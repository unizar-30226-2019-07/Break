# crea el objeto app como una instancia de la class Flask
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

from app import routes