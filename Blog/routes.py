import secrets
import os
from flask import render_template, url_for, flash, redirect, request, abort
from Blog import app, db, bcrypt, mail
from Blog.forms import (RegistrationForm, LoginForm,
UpdateAccountForm, TodoForm,
RequestResetForm, ResetPasswordForm)
from Blog.models import User, Todo
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date
# import pillow to process images
from PIL import Image
from flask_mail import Message


# home page, containing all todo items
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
@login_required
def home ():
    finish = request.args.get('finish', "unfinished", type=str)
    order = request.args.get('order', "created", type=str)
    page = request.args.get('page', 1, type = int)
    if finish == "finished":
        todos = Todo.query.filter_by(author=current_user, finished=True).order_by(Todo.date_finished.desc()).paginate(per_page = 5, page = page)

        home_status = {
            "days":0,
            "curr_position": "Home Page",
            "events":[
                "<span>You can apply opertions by clicking various buttons</span>",
                f'<span class="sidebar-font">Finished Number: </span>{Todo.query.filter_by(author = current_user, finished = True).count()}',
                f'<span class="sidebar-font">Unfinished Number: </span> {Todo.query.filter_by(author = current_user, finished = False).count()}'
            ]
        }

    elif finish == "unfinished":
        if order == "created":
            todos = Todo.query.order_by(Todo.date_posted.desc()).filter_by(author=current_user, finished=False).paginate(per_page = 5, page = page)
        elif order == "left":
            todos = Todo.query.order_by(Todo.deadline.asc()).filter_by(author=current_user, finished=False).paginate(per_page = 5, page = page)
        else:
            abort(404)
            
        for todo in todos.items:
            temp_days_left = (todo.deadline - date.today()).days
            if temp_days_left >= 0:
                todo.days_left = f'{(todo.deadline - date.today()).days} days left'
                todo.delay = False
            else:
                todo.days_left = "Time out !"
                todo.delay = True

        home_status = {
            "days":0,
            "curr_position": "Home Page",
            "events":[
                "<span>You can apply opertions by clicking various buttons</span>",
                f'<span class="sidebar-font">Finished Number: </span>{Todo.query.filter_by(author = current_user, finished = True).count()}',
                f'<span class="sidebar-font">Unfinished Number: </span> {Todo.query.filter_by(author = current_user, finished = False).count()}'
            ]
        }
    else:
        abort(404)

    return render_template('home.html', title="Home", todos = todos, finish=finish, status = home_status)


@app.route('/about')
def about ():
    return render_template('about.html', title="about")


@app.route('/register', methods=["GET", "POST"])
def register ():
    #判断当前是否有用户登录:
    if current_user.is_authenticated:
        flash("Already Login", 'info')
        return redirect(url_for('home'))

    form = RegistrationForm()

    # 判断, 如果提交的表单有问题的话, 就直接调用flash方法, 上传一个
    if form.validate_on_submit():
        # flash的第二个参数: categroy, 可以理解为一个属性, 用于描述当前的通知, 在这里, 它的另一个用途是作为bootstrap的类名来改变元素的样式, 很是方便;
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are ready to log in !','success')
        return redirect(url_for('login'))
    # else:
    #     flash()
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=["GET", "POST"])
def login ():
    if current_user.is_authenticated:
        flash("Already Login", 'info')
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) # 登录在这里完成
            flash(f"Welcome! {user.username}", 'success')
            # 这个的作用是让浏览器返回用户之前被阻挡的那个页面
            # 这个next就是网址里的那个?next, 类似于携带的一个参数, 可以直接访问
            # 若没有next, 那就代表是正常login; 而非由于未登录而被强制转向login;
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash("Unsuccessful Login! Please check you email or password !", 'danger')

    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        flash('logout successfully', 'success')
        logout_user() # 用户退出
        return redirect(url_for('login'))
    
    flash('You need to login first !', 'info')
    return redirect(url_for('login'))


# 用于将用户上传的图片保存至本地服务器, 这里的form_picture参数是一个filestorage类型, 需要通过.filename来获取文件名
def save_picture(form_picture):
    # 通过随机字符串创建文件名;
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    # 似乎在提交表单的时候, account()函数会被调用两次, 第一次是post, 第二次是get, 这也解释了为什么要在这里加一个判断条件
    # 如果没有这个判断, 在post请求时, 所有用户填入的更新信息都会被重置为原来的用户名和邮箱;

    # place original information in the form
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    if form.validate_on_submit():
        if form.picture.data:
            # if the original image is not the default one, just delete it
            if current_user.image_file != "default.jpg":
                current_picture_path = os.path.join(app.root_path, "static/profile_pics", current_user.image_file)
                os.remove(current_picture_path)
            
            # 这里穿进去的是个图片, 而不是图片的文件名 !!;
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated !", "success")
        return redirect(url_for('account'))

    days = (date.today() - current_user.date_created).days+1

    account_status = {
        "days": days,
        "curr_position": "Account Page",
        "events":[
            "<span>View or update your personal account info</span>",
            f'<span class="sidebar-font">Finished Number:  {Todo.query.filter_by(author = current_user, finished = True).count()}</span>',
            f'<span class="sidebar-font">Unfinished Number:  {Todo.query.filter_by(author = current_user, finished = False).count()}</span>'
        ]
    }

    image_file = url_for('static',filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Account",
                           image_file=image_file, form = form, status = account_status)


# add one new todo item
@app.route('/new_todo', methods=["GET", "POST"])
@login_required
def new_todo():
    form = TodoForm()

    if form.validate_on_submit():
        todo = Todo(title=form.title.data, content=form.content.data, author=current_user, deadline=form.deadline.data, date_posted = datetime.now())
        db.session.add(todo)
        db.session.commit()
        flash("Your todo has been created !", 'success')
        return redirect(url_for('home'))
    
    todo_status = {
        "days":0,
        "curr_position": "Todo Page",
        "events":[
            "<span>Start a new todo by filling the form</span>",
            "<span>Remember that deadline should not be set before today !</span>",
            f'<span class="sidebar-font">Finished Number: </span>{Todo.query.filter_by(author = current_user, finished = True).count()}',
            f'<span class="sidebar-font">Unfinished Number: </span> {Todo.query.filter_by(author = current_user, finished = False).count()}'
        ]
    }
    
    return render_template('create_todo.html', title="New Todo", form=form, legend="New Todo", status=todo_status)


# delete one todo item
@app.route('/todo/<int:todo_id>/update', methods=["GET", "POST"])
@login_required
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    form = TodoForm()

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.content = form.content.data
        todo.deadline = form.deadline.data
        db.session.commit()
        flash("Your todo has been updated !", 'success')
        return redirect(url_for('home'))
    elif request.method == "GET":
        form.title.data = todo.title
        form.content.data = todo.content
        form.deadline.data = todo.deadline
        
    return render_template('create_todo.html', title="Update Todo",
                           form = form, legend = "Update Todo")


# delete one todo item
@app.route('/todo/<int:todo_id>/<finish>/delete', methods=["POST"])
@login_required
def delete_todo(todo_id, finish):
    print(todo_id)
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash("Your todo has been deleted !", 'success')
    return redirect(url_for('home', finish=finish))


# finish one todo item
@app.route('/finish_todo/<int:todo_id>')
@login_required
def finish_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if current_user == todo.author:
        todo.finished = True
        todo.date_finished = datetime.now()
        if todo.deadline >= todo.date_finished.date(): # not finishing this on time
            todo.on_time = True
        else:
            todo.on_time = False
        db.session.commit()
        flash("Finish one todo !", 'success')
    else:
        abort(403)
    return redirect(url_for('home'))


# used for debugging

@app.route('/test')
def test ():
    return current_user.username


# 用于发送邮件
def send_reset_email(user):
    token = user.get_reset_token() # 默认半小时
    msg = Message('Password Reset Request',
                  sender='1013752750@qq.com',
                  recipients=[user.email])
    msg.body = f'''To reset you password, visit the following link:

{url_for('reset_token', token=token, _external=True)}

If you didn't make this request them just ignore it
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # 确保用户在登录的情况下, 不会载入此页;
    if current_user.is_authenticated:
        flash("Already Login", 'info')
        return redirect(url_for('home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title="Reset Password", form = form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash("Already Login", 'info')
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('Invalid or expired token !', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You are now able to login.','success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title="Reset Password", form = form)


@app.route('/mail_test')
def mail_test():
    msg = Message('message testing', sender="1013752750@qq.com", recipients=['olym_ding@163.com'])
    msg.body = 'wow ! success !'
    mail.send(msg)

    return redirect('home')