from flask import Flask

app = Flask(__name__)

import appconfig

from models import db
db.init_app(app)
from app import views