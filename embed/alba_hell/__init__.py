from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://embed_admin:1234@113.198.235.225/embed'
app.config['LOGGING_LEVEL'] = logging.DEBUG
app.config['SECRET_KEY'] = 'this is secret!!'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


from alba_hell import auth
from alba_hell import views
from alba_hell import attendance
from alba_hell import temperature
from alba_hell import camera
