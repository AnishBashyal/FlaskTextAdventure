from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error.html', error = "Page doesn't exist!"), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error.html', error = "You don't have permission to do so!"), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error.html', error = "Something Wrong!"), 500
