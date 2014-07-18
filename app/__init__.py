from flask import Flask
import flask.ext.whooshalchemy

app = Flask(__name__)

import appconfig

from models import db, Document, CityRecord
db.init_app(app)

with app.app_context():
	flask.ext.whooshalchemy.whoosh_index(app, Document)
	flask.ext.whooshalchemy.whoosh_index(app, CityRecord)

from app import views