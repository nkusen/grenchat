from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import jwt
import os
from time import time

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __bind_key__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(50))

    def get_reset_token(self, expires=500):
        return jwt.encode({"reset_password": self.name,
                           "exp": time() + expires}, 
                           current_app.config["SECRET_KEY"], algorithm="HS256")
    
    def verify_reset_token(token):
        try:
            name = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['reset_password']
        except Exception as e:
            print(e)
            return
        return User.query.filter_by(name=name).first()

class Message(db.Model):
    __bind_key__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    content = db.Column(db.String(800))
    time = db.Column(db.DateTime, default=datetime.now)
