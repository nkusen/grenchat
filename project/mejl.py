from flask import current_app, render_template
from flask_mail import Mail, Message

mail = Mail()

def send_email(user):
    token = user.get_reset_token()
    with current_app.app_context():
        msg = Message()
        msg.subject = "Password reset"
        msg.sender = current_app.config['MAIL_USERNAME']
        msg.recipients = [user.email]
        msg.html = render_template("reset_email.html", user=user, token=token)
        mail.send(msg)
        print("Sent to: " + user.email)