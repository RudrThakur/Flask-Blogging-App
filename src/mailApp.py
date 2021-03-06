from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'rudrakshchandramukut@gmail.com',
    "MAIL_PASSWORD": 'rudrcmkt777'
}

app.config.update(mail_settings)
mail = Mail(app)

def sendVerificationEmail(userEmail, verificationCode):
    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[userEmail], # replace with your email for testing
                      body="Your Verification Code is " + verificationCode)
        mail.send(msg)