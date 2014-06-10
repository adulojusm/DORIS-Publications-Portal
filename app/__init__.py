from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config_default
import sqlite3


app = Flask(__name__)
app.config.from_pyfile('config_default.py')
db = SQLAlchemy(app)
from main import views
from app import models




