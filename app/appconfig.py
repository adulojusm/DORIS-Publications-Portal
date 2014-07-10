from app import app

import mysql_config

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/publications' % (mysql_config.username, mysql_config.password, mysql_config.hostname)
app.config['SESSION_COOKIE_NAME'] = 'active'
app.config['SECRET_KEY'] = 'F34TF$($e34D'