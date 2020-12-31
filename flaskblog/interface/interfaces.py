from flaskblog import api
from flask_login import current_user, login_required
from flask_restful import Resource
from flask import Blueprint
from flaskblog.models import Like

interfaces = Blueprint('interfaces', __name__)

@interfaces.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like(post_id):
    print(current_user.id)
    return str(3)