from flaskblog import api
from flask_restful import Resource
from flask import Blueprint

interfaces = Blueprint('interfaces', __name__)

@interfaces.route("/like/<int:post_id>", methods=["POST"])
def like(post_id):
    print(post_id)
    return {'test': 'wow'}