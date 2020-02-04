from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from pymongo import MongoClient
from datetime import datetime
import re

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '1234'

client = MongoClient('mongodb+srv://rudrthakur:rudrcmkt777@rudr-vh5fo.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = client.rudr

@app.route('/')
def home():
    if 'username' not in session:
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    usersDB = db.users
    usersList = usersDB.find_one({'username': request.form['username']} and {'password': request.form['password']})
 
    if usersList is not None:
        userProfile = {'username': request.form['username'], 'password' : request.form['password']}
        session['username'] = userProfile['username']
        return home()
    else:
        return('User Not Found')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)