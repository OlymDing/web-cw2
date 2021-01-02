from flask import render_template, request, Blueprint, current_app, Response,redirect, url_for
from flaskblog.models import Post
from flask_login import current_user
from flaskblog.main.forms import SettingForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, test=True)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/settings", methods=['GET', 'POST'])
def settings():
    settings = SettingForm()
    resp = Response(render_template('settings.html', title='Settings', form = settings, legend = "Settings"))
    if settings.validate_on_submit():
        print(settings.color.data)
        resp.set_cookie('color', settings.color.data)
        resp.set_cookie('username', 'djq')
        return redirect(url_for('main.home'))
    else:
        return resp