from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from celery import Celery
from datetime import datetime
import re
import hashlib, binascii
from downloaderApp import *
from db import *


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '1234'

#home
@app.route('/')
def home():
    if 'name' not in session:
        return render_template('login.html')
    else:
        usersDB = database()
        userProfile = usersDB.find_one({'username' : session['username']})
        flash('Logged In Successfully')
        return render_template('index.html', userProfile = userProfile)


#login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if not (request.form['username'] and request.form['password']):
            flash('Please Fill All the credentials')
            return render_template('login.html')

        else:
            usersDB = database()
            userData = usersDB.find_one({'username': request.form['username']})

            if userData:
                if verify_password(userData['password'], request.form['password']):
                    usersDB = database()
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
    else:
        return render_template('login.html')

def verify_password(stored_password, provided_password):

    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

#register
@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        if not (request.form['username'] and request.form['password'] and request.form['name'] and
        request.form['email'] and request.form['phone'] and
        request.form['city'] and request.form['occupation']):
            flash('Please Fill All the credentials')
            return render_template('register.html')

        else:
            usersDB = database()
            usersList = usersDB.find_one({'username': request.form['username']})
            
            if usersList is None:
                userInsert = usersDB.insert_one( { 'username': request.form['username'], 'name': request.form['name'], 
                'password': hash_password(request.form['password']), 'email': request.form['email'], 'phone': request.form['phone'],
                'city': request.form['city'], 'occupation': request.form['occupation']} )
                session['username'] = request.form['username']
                session['name'] = request.form['name']
                return home()
            else:
                flash('Username Already Exists !')
                return render_template('register.html')
    else:
        return render_template('register.html')

def hash_password(password):

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

#change user password
@app.route('/changepassword', methods=['POST'])
def changeUserPassword():
    usersDB = database()
    userData = {'username':  session['username']}
    updatePassword = { '$set' : {'password' : hash_password(request.form['new_password'])}}
    if usersDB.update(userData, updatePassword):
        flash('Password Updated')
    else:
        flash('Password Update Failed')
    return redirect('/')


#logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html')

#main
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)