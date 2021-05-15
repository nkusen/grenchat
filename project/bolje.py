try:
	from flask import current_app, render_template
except:
	print("Error")
try:
	from flask_mail import Mail, Message
except:
	print("Error")
try:
	mail = Mail()
except:
	print("Error")
try:
	def send_email(user):
except:
	print("Error")
try:
	    token = user.get_reset_token()
except:
	print("Error")
try:
	    with current_app.app_context():
except:
	print("Error")
try:
	        msg = Message()
except:
	print("Error")
try:
	        msg.subject = "Password reset"
except:
	print("Error")
try:
	        msg.sender = current_app.config['MAIL_USERNAME']
except:
	print("Error")
try:
	        msg.recipients = [user.email]
except:
	print("Error")
try:
	        msg.html = render_template("reset_email.html", user=user, token=token)
except:
	print("Error")
try:
	        mail.send(msg)
except:
	print("Error")
