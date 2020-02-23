from flask import render_template

from interface import app


@app.errorhandler(404)
def page_not_found(err):
    # return render_template("url"),状态码
    # return render_template('404.html'), 404
    return render_template('404.html'), 404


@app.errorhandler(401)
def authorized_page(err):
    return render_template('401.html'), 401
