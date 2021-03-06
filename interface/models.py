# -*- coding: utf-8 -*-
"""
    :author: Zijun Huang
"""

from datetime import datetime

from interface import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class Message(db.Model, UserMixin):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class User(db.Model, UserMixin):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    school = db.Column(db.String(50))
    #name = db.Column(db.String(30))
    mathmodel = db.relationship('Mathmodel', back_populates='user')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Mathmodel(db.Model, UserMixin):
    __tablename__ = "mathmodel"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='mathmodel')
