from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta
from models import db, User, Message
from mejl import send_email

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Wrong password or user doesn't exist.")
            return redirect(url_for("auth.login"))
        
        login_user(user, remember=remember, duration=timedelta(days=30))
        return redirect(url_for("main.chat"))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email address already exists")
            return redirect(url_for("auth.signup"))
        
        new_user = User(email=email, name=name, password=generate_password_hash(password, method="sha256"))
        
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/delete")
@login_required
def delete_user():
    user = User.query.filter_by(email=current_user.email).first()
    db.session.delete(user)
    db.session.commit()
    return logout()

@auth.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == "GET":
        return render_template("reset.html")
    else:
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email address not in database")
            return redirect(url_for("auth.reset"))
        else:
            send_email(user)
            return redirect(url_for("auth.login"))

@auth.route("/verify/<token>", methods=["GET", "POST"])
def verify(token):
    if request.method == "GET":
        return render_template("reset_verify.html")
    else:
        user = User.verify_reset_token(token)
        if not user:
            return redirect(url_for("auth.login"))
        password = request.form.get("password")
        user.password = generate_password_hash(password, method="sha256")
        
        print(password, user.password, user.email)

        db.session.commit()

        new_user = User.query.filter_by(name=user.name).first()
        print(new_user.name, new_user.email, new_user.password)

        return redirect(url_for("auth.login"))
