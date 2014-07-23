from flask import Flask
import flask.ext.whooshalchemy

app = Flask(__name__)

import appconfig

from models import db, Document
db.init_app(app)

with app.app_context():
	flask.ext.whooshalchemy.whoosh_index(app, Document)

from app import views