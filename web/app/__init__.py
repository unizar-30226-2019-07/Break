# crea el objeto app como una instancia de la class Flask
from flask import Flask

app = Flask(__name__)

from app import routes