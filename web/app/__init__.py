# crea el objeto app como una instancia de la class Flask
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
