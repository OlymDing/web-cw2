# import database instance and login 
from Todo import db, login_manager, app
from datetime import datetime, date
# make default user setting
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.Date, nullable = False, default = date.today())
    todos = db.relationship('Todo', backref='author', lazy=True)

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec) # 创建序列化实例
        return s.dumps({'user_id': self.id}).decode('utf-8') # 返回口令实例

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] # 如果仍在时间范围内, 就可以解码成功, 并且返回一个装有user_id的字典
        except: # 若有问题, 就说明时间过了
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.now())
    deadline = db.Column(db.Date, nullable = False)
    date_finished = db.Column(db.DateTime, nullable = True)
    finished = db.Column(db.Boolean, nullable = False, default = False)
    on_time = db.Column(db.Boolean, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Todo('{self.title}', '{self.date_posted}')"