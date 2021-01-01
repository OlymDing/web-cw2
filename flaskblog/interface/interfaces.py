from flaskblog import api, db
from flask_login import current_user, login_required
from flask_restful import Resource
from flask import Blueprint, flash, jsonify, request
from flaskblog.models import Like, Post, Comment
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

@interfaces.route("/make_comment/<int:post_id>", methods=["POST"])
def make_comment(post_id):
    if current_user.is_authenticated:
        comment_str = request.form.get('comment')
        new_comment = Comment(content = comment_str, user_id = current_user.id, post_id = post_id)
        db.session.add(new_comment)
        db.session.commit()
    return jsonify({'content': new_comment.content, 'time': new_comment.date_commented, 'user_id': new_comment.user_id })

@interfaces.route("/get_comments/<int:post_id>")
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id = post_id).all()
    comment_list = []
    for i in comments:
        comment_list.append({'content': i.content, 'time': i.date_commented, 'user_id': i.user_id })
    return jsonify({'data': comment_list})