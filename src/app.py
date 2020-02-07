from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import random
from celery import Celery
from datetime import datetime
import re
import hashlib, binascii
from taskworker import *
from db import *
from mailapp import *


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '1234'
usersDB = databaseUsers()

#home
@app.route('/')
def home():
    if 'name' not in session:
        return render_template('login.html')
    else:
        userProfile = usersDB.find_one({'username' : session['username']})

        if userProfile['isActive']:
            flash('Logged In Successfully')
            return render_template('index.html', userProfile = userProfile)
        else:
            flash('Please Verify Your Account')
            return render_template('verifyaccount.html', userProfile = userProfile)


#login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if not (request.form['username'] and request.form['password']):
            flash('Please Fill All the credentials')
            return render_template('login.html')

        else:
            userData = usersDB.find_one({'username': request.form['username']})

            if userData:
                if verify_password(userData['password'], request.form['password']):
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
            usersList = usersDB.find_one({'username': request.form['username']})
            
            if usersList is None:
                verificationCode = generateVerificationCode()
                sendVerificationEmail(request.form['email'], verificationCode)
                userInsert = usersDB.insert_one( { 'username': request.form['username'], 'name': request.form['name'], 
                'password': hash_password(request.form['password']), 'email': request.form['email'], 'phone': request.form['phone'],
                'city': request.form['city'], 'occupation': request.form['occupation'], 'isActive': False, 
                'verificationcode': verificationCode} )
                session['username'] = request.form['username']
                session['name'] = request.form['name']
                flash('The Verification Code has been Sent to your email Account')
                return home()
            else:
                flash('Username Already Exists !')
                return render_template('register.html')
    else:
        return render_template('register.html')

def generateVerificationCode():
    code = random.randrange(1, 500000, 1)
    return hash_password(str(code))

def hash_password(password):

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

#change user password
@app.route('/changepassword', methods=['POST', 'GET'])
def changeUserPassword():
    if request.method == 'POST':
        userIndex = {'username':  session['username']}
        newUserPassword = { '$set' : {'password' : hash_password(request.form['new_password'])}}
        if usersDB.update(userIndex, newUserPassword):
            flash('Password Updated')
        else:
            flash('Password Update Failed')
        return redirect('/')
    else:
        userProfile = usersDB.find_one({'username': session['username']})
        return render_template('changepassword.html', userProfile = userProfile)

#verify Account
@app.route('/verifyaccount', methods=['POST'])
def verifyUserAccount():
    userProfile = usersDB.find_one({'username': session['username']})

    if request.form['verification_code'] == userProfile['verificationcode']:
        userIndex = {'username':  session['username']}
        newUserState = { '$set' : {'isActive' : True}}
        nullifyVerificationCode = { '$set' : {'verificationcode' : None}}
        if usersDB.update(userIndex, newUserState):
            flash('Account Verified Successfully')
            usersDB.update(userIndex, nullifyVerificationCode)
        else:
            flash('Account Verification Failed')

    return redirect('/')

#logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html')

#main
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)