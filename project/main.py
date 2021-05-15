from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, User, Message

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/index")
@main.route("/home")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

@main.route("/chat")
@login_required
def chat():
    return render_template("chat.html", name=current_user.name)

@main.route("/history")
@login_required
def history():
    messages = Message.query.order_by(Message.time).all()
    return render_template("history.html", messages=messages)

@main.route("/about")
def about():
    return render_template("about.html")
