from flask import render_template, request, Blueprint, current_app, Response,redirect, url_for
from flaskblog.models import Post
from flask_login import current_user
from flaskblog.main.forms import SettingForm
from datetime import date

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if current_user.is_authenticated:
        sidebar_info = []
        sidebar_info.append(f"Hi {current_user.username} !")
        sidebar_info.append(f'You have been here for {(date.today() - current_user.date_created).days + 1} days')
        sidebar_info.append('Share your life by writting a post !')
        return render_template('home.html', posts=posts, sidebar_info=sidebar_info)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/settings", methods=['GET', 'POST'])
def settings():
    settings = SettingForm()
    sidebar_info = ['Modify the color of your web !']
    return render_template('settings.html', title='Settings', form = settings, legend = "Settings", sidebar_info = sidebar_info)