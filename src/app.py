from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '1234'

@app.route('/')
def home():
    if not session.get('isLoggedIn'):
        return render_template('login.html')
    else:
        return "Hello User!"

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['isLoggedIn'] = True
    else:
        flash('Invalid Credentials!')
        return home()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)