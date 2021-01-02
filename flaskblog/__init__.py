from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
import logging
from flask.logging import default_handler
import os

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


app = Flask(__name__)
app.config.from_object(Config)

# initial api;

app.logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('./flaskblog/static/record.log')
file_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
app.logger.addHandler(file_handler)

db = SQLAlchemy(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.handlers import errors
from flaskblog.interface.interfaces import interfaces
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(interfaces)