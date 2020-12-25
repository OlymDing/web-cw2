from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import pymysql
import os

app = Flask(__name__)
# 设置秘钥?
app.config['SECRET_KEY'] = '1287ff70f6a4f5bbdd2e690506b03134'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dingjianqiao@localhost:3306/mydb'
db = SQLAlchemy(app) # 创建数据库实例
bcrypt = Bcrypt(app) # 创建加密实例
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL']=True

# 环境变量, 来存储用户的隐私信息, 如邮箱和密码
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

from Todo import routes