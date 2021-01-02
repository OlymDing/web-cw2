from flask import Blueprint, render_template, current_app

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    current_app.logger.error("404 error")
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    current_app.logger.error("403 error")
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    current_app.logger.error("Server Internal Error !")
    return render_template('errors/500.html'), 500
