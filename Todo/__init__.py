# basic flask instance;
from flask import Flask
# handles DB mapping;
from flask_sqlalchemy import SQLAlchemy
# handles crypting;
from flask_bcrypt import Bcrypt
# handles login, such as forbidding viewing one page if not logged in;
from flask_login import LoginManager
# handles sending mail
from flask_mail import Mail

import os

app = Flask(__name__)
# one general secret key, which helps when a third party plugin is applied;
app.config['SECRET_KEY'] = '1287ff70f6a4f5bbdd2e690506b03134'
# the address of the database;
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) # create database instance;
bcrypt = Bcrypt(app) # create one crypt instance;
login_manager = LoginManager(app) # create one login managing instance;
login_manager.login_view = 'login' # redirect view name;
login_manager.login_message_category = "info" # type of message;

# mail setting;
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL']=True

# host's email username and password;
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app) # initialize the Mail instance

from Blog import routes