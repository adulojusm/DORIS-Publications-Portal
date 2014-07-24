from flask import Flask
import flask.ext.whooshalchemy
from flask.ext.mail import Mail

mail = Mail()

app = Flask(__name__)
mail.init_app(app)


import appconfig

from models import db, Document
db.init_app(app)

with app.app_context():
	flask.ext.whooshalchemy.whoosh_index(app, Document)

from app import views