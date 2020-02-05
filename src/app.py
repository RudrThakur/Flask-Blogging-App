from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from celery import Celery
from pymongo import MongoClient
from datetime import datetime
import re
from downloaderApp import *

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '1234'

client = MongoClient('mongodb+srv://rudrthakur:rudrcmkt777@rudr-vh5fo.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = client.rudr

@app.route('/')
def home():
    if 'name' not in session:
        return render_template('login.html')
    else:
        usersDB = db.users
        userProfile = usersDB.find_one({'username' : session['username']})
        flash('Logged In Successfully')
        return render_template('index.html', userProfile = userProfile)

@app.route('/login', methods=['POST'])
def login():

    if not (request.form['username'] and request.form['password']):
        flash('Please Fill All the credentials')
        return render_template('login.html')

    else:

        usersDB = db.users
        userData = usersDB.find_one({'username': request.form['username']})

        if userData:
            if userData['password'] == request.form['password']:
                usersDB = db.users
                userProfile = usersDB.find_one({'username': request.form['username']})
                session['username'] = userProfile['username']
                session['name'] = userProfile['name']
                logLastLogin.delay(session['username'])
                return home()
            else:
                flash('Invalid Credentials')
                return render_template('login.html')
        else:
            flash('User Not Found')
            return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():

    if not (request.form['username'] and request.form['password'] and request.form['name'] and
    request.form['email'] and request.form['phone'] and
    request.form['city'] and request.form['occupation']):
        flash('Please Fill All the credentials')
        return render_template('register.html')

    else:

        usersDB = db.users
        usersList = usersDB.find_one({'username': request.form['username']})
        
        if usersList is None:
            userInsert = usersDB.insert_one( { 'username': request.form['username'], 'name': request.form['name'], 
            'password': request.form['password'], 'email': request.form['email'], 'phone': request.form['phone'],
            'city': request.form['city'], 'occupation': request.form['occupation']} )
            session['username'] = request.form['username']
            session['name'] = request.form['name']
            return home()
        else:
            return('Username Already Exists !')

@app.route('/registrationpage', methods=['GET'])
def registerationpage():
    return render_template('register.html')

@app.route('/loginpage', methods=['GET'])
def loginpage():
    return render_template('login.html')

@app.route('/changepassword', methods=['POST'])
def changeUserPassword():
    usersDB = db.users
    userProfile = usersDB.find_one({'username': session['username']})
    updateStatus = changePassword.delay(session['username'], request.form['password'])
    if updateStatus:
        flash('Password Update Successfully')
        return render_template('index.html', userProfile = userProfile)
    else:
        flash('Sorry Something Went Wrong !')
        return render_template('index.html', userProfile = userProfile)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)