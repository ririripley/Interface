# -*- coding: utf-8 -*-
"""
    :author: Ripley
"""
#from os import abort

from flask import abort
from flask import flash, redirect, url_for, render_template, request
from flask import session
from flask import jsonify
from interface import app, db
from interface.models import Message, User, Mathmodel
from interface.utils import verify_token, generate_token, allowed_file
from interface.emails import send_confirm_email, send_reset_password_email, send_change_email_email


from flask_login import login_user, login_required
from flask_login import current_user
from flask_login import logout_user
from flask_login import UserMixin
# from werkzeug import secure_filename

# test1
@app.route('/firstpage', methods=['GET','POST'])
def welcome():
    if request.method == 'GET':
        return "Hello, world!"
    else:
        data = request.get_json()
        username = data['username']
        return username
        #return "what the fuck did you send to me?"
#http://127.0.0.1:5000/

@app.route('/PageNotFound')
def PageNotFound():
    abort(404)


@app.route('/UnauthorizedPage')
def UnauthorizedPage():
    abort(401)


# test 2
@app.route('/postQUE', methods=['POST'])
def sendQUE():
    data = request.get_json()
    username = data['username']
    return jsonify({'success':username})



@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)  #错误设置有问题
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
            #abort(400)
            flash('Repeated email!', 'warning')
            return jsonify({'register': False})

    # validate username
        if User.query.filter_by(username=username).first():
            flash('Repeated Username!','warning')
            return jsonify({'register': False})
            #abort(400)

        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        #token = generate_token(user=user, operation='confirm')
        #send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        # return jsonify({ 'username': user.username }), 200, {'Location': url_for('get_user', id = user.id, _external = True)}
        return jsonify({'register':True})


@app.route('/users/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"login": True})
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if user is not None and user.validate_password(password):
            login_user(user)
            print(current_user.get_id())
            print(session)
            # flash('Login success.', 'info')
            return jsonify({"login": True, "time" : 2})
        else:
            # flash('Invalid email or password.', 'warning')
            return jsonify({"login": False})

@app.route('/users/logout')
@login_required
def logout():
    #print(session)
    #print(current_user.id)
    logout_user()
    #print("asdf")
    # flash('Logout success.', 'info')
    return jsonify({"logout": True})




@app.route('/users/reset-password',  methods=['GET','POST'])
@login_required
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html')

    data = request.get_json()
    original_password = data['original_password']
    new_password1 = data['password1']
    new_password2 = data['password2']

    if current_user.validate_password(original_password):
        if (new_password1 == new_password2):
            if (new_password1 != original_password):
                current_user.set_password(new_password1)
                db.session.commit()
                logout_user()
                return jsonify({"reset_password": True})
            else:
                flash('Please make sure you new password is different the original one!')
        else:
            flash('Please make sure the two new passwords you input are the same!')
    else:
        flash('Invalid email or password.', 'warning')
    return jsonify({"reset_password": False})


@app.route('/users/reset-username',  methods=['GET','POST'])
@login_required
def reset_username():
    if request.method == 'GET':
        return render_template('reset_username.html')

    data = request.get_json()
    new_username = data['new_username']

    if(current_user.username == new_username):
        flash('Please make sure the you enter a different username from the current one!')
        return jsonify({"reset_username": False})
    current_user.username = new_username
    db.session.commit()
    return jsonify({"reset_username": True})

@app.route('/users/reset-email',  methods=['GET','POST'])
@login_required
def reset_email():
    if request.method == 'GET':
        return render_template('reset_email.html')

    data = request.get_json()
    password = data['password']
    new_email= data['new_email']

    if current_user.validate_password(password):
        if (current_user.email != new_email):
            current_user.email = new_email
            db.session.commit()
            return jsonify({"reset_email": True})
        else:
            flash('Please make sure the you enter a different email from the current one!')
    else:
        flash('Invalid email or password.', 'warning')
    return jsonify({"reset_email": False})


@app.route('/users/info', methods=['GET'])
@login_required
def get_user_info():
    return jsonify({"username":current_user.username, "email":current_user.email})


'''
@app.route('/upload_file/<string:title>', methods=['GET', 'POST'])
@login_required
def upload(title):
    if request.method == 'GET':
        return render_template('upload.html')
    file = request.files['file']  # 'file'为前端定义的变量名
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return jsonify({"upload file": None})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mathmodel = Mathmodel(title = title, body = (os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        mathmodel.user = current_user
        return jsonify({"user_id""upload file": True})
    return jsonify({"upload file": False})
'''
