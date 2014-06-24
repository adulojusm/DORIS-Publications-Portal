from flask import Flask
import mysql_config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/publications' % (mysql_config.username, mysql_config.password, mysql_config.hostname)

from models import db
db.init_app(app)
from app import views