from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@10.132.41.31/publications'

from models import db
db.init_app(app)
from app import views