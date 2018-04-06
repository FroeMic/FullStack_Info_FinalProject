from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login = LoginManager(app)

from app import routes, models, forms, utils


def _create_database():
    ''' Creates the database schema specified by the SQLAlchemy models '''
    print('Rebuilding database schema ... ')
    db.create_all()
    print('Done!')