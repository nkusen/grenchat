import json
import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, send
from datetime import datetime
from models import db
from mejl import mail

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["transports"] = "websocket"
app.config["SQLALCHEMY_BINDS"] = {
    "users": os.environ.get("DATABASE_URL")[:8] + "ql" + os.environ.get("DATABASE_URL")[8:], 
    "messages": os.environ.get("HEROKU_POSTGRESQL_CYAN_URL")[:8] + "ql" + os.environ.get("HEROKU_POSTGRESQL_CYAN_URL")[8:]}
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "grenchat@gmail.com"
app.config['MAIL_PASSWORD'] = os.environ.get("PASSWORD")

mail.init_app(app)

db.app = app
db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

from models import User, Message

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from main import main
app.register_blueprint(main)

from auth import auth
app.register_blueprint(auth)

@socketio.on("disconnect")
def disconnected():
    data = {"content": f"{current_user.name} has disconnected...",
            "user": "",
            "time": datetime.now().strftime('%I:%M%p')}
    send(data, json=True, broadcast=True)

@socketio.on("connect")
def connected():
    data = {"content": f"{current_user.name} has connected!",
            "user": "",
            "time": datetime.now().strftime('%I:%M%p')}
    send(data, json=True, broadcast=True)

@socketio.on("message")
def handleMessage(msg):
    data = {"content": msg,
            "user": current_user.name,
            "time": datetime.now().strftime('%I:%M%p')}
    send(data, json=True, broadcast=True)
    new_message = Message(user=current_user.name, content=msg)
    db.session.add(new_message)
    db.session.commit()

if __name__ == "__main__":
    socketio.run(app, port=int(os.environ.get("PORT", 33507)))
