from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from grocery_app.config import Config
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

###########################
# Authentication
###########################

# TODO: Add authentication setup code here!
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)