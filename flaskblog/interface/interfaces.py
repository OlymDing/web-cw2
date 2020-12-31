from flaskblog import api, db
from flask_login import current_user, login_required
from flask_restful import Resource
from flask import Blueprint, flash, jsonify
from flaskblog.models import Like, Post
from sqlalchemy.exc import DatabaseError

interfaces = Blueprint('interfaces', __name__)

@interfaces.route("/like/<int:post_id>", methods=["POST"])
def like(post_id):
    #login_required 应该是直接修改返回值, 但对于这种接口而言, 只能使用is_authenticated来判断;
    if current_user.is_authenticated:
        #1. 先判断之前是否点过赞
        like = Like.query.get((current_user.id, post_id))
        # 已经点过赞了:
        if like:
            db.session.delete(like)
            count = Like.query.filter_by(post_id = post_id).count()
            Post.query.get(post_id).likes = count
            db.session.commit()
            return jsonify({'founded': True, 'count':count})
        # 还没有点赞:
        else:
            like = Like(user_id = current_user.id, post_id = post_id)
            db.session.add(like)
            count = Like.query.filter_by(post_id = post_id).count()
            Post.query.get(post_id).likes = count
            db.session.commit()
            return jsonify({'founded': False, 'count':count})
    else:
        return jsonify({'founded': False})