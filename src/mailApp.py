from flask import Flask
from flask_mail import Mail, Message
from flask import current_app  # use this to reference current application context

app = Flask(__name__)
mail = Mail(app)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '1234'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rudrakshchandramukut@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'rudrakshchandramukut@gmail.com' # enter your email here
app.config['MAIL_PASSWORD'] = 'rudrcmkt777' # enter your password here

def send_email(email_data):
    msg = Message(sender='rudrakshchandramukut@gmail.com',
                  recipients='rudrakshacmkt777@gmail.com')
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)