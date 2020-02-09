# -*- coding: utf-8 -*-
"""
    :author: Ripley
"""
from os import abort

from flask import flash, redirect, url_for, render_template, request
from flask import jsonify
from interface import app, db
from interface.models import Message, User, Mathmodel
from interface.utils import verify_token, generate_token
from interface.emails import send_confirm_email, send_reset_password_email, send_change_email_email



@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/users/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

    #validate email address
        if User.query.filter_by(email=email).first():
            abort(600)

    # validate username
        if User.query.filter_by(username=username).first():
            abort(601)

        user = User(name=name, email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        return jsonify({ 'username': user.username }), 200, {'Location': url_for('get_user', id = user.id, _external = True)}


@app.route('/users/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if user is not None and user.validate_password(password):
            flash('Login success.', 'info')
            return jsonify({"login": True})
        else:
            flash('Invalid email or password.', 'warning')
            return jsonify({"login": False})


@app.route('/users/logout')
