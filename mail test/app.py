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

@app.route('/')
def home():
    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["rudrakshacmkt777@gmail.com"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)
    return ('hello !')

#main
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)