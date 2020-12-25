from Todo import db, bcrypt
from Todo.models import User, Todo
from datetime import *
import os

db.create_all()

hashed_pw1 = bcrypt.generate_password_hash("admin").decode('utf-8')
hashed_pw2 = bcrypt.generate_password_hash("testing").decode('utf-8')


user1 = User(username = "admin", email = "admin@qq.com", password = hashed_pw1)
user2 = User(username = "test", email = "test@demo.com", password = hashed_pw2)

db.session.add(user1)
db.session.add(user2)

ddl = date(2020,12,10)
ddl1 = date(2020,12,20)

todo1 = Todo(title="好好学习", content="好好学习, 天天向上", author = user1, deadline=ddl)
todo2 = Todo(title="打扫卫生", content="房间的卫生状况太糟糕了! 赶紧回去打扫卫生.", author = user1, deadline=ddl1)

db.session.add(todo1)
db.session.add(todo2)

db.session.commit()
