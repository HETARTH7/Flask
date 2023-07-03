from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://db:27017/flaskdb'
mongo = PyMongo(app)

from app.resources import api
api.init_app(app)
