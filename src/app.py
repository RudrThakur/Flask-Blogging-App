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
    if 'name' not in session:
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

    if not (request.form['username'] or request.form['password']):
        return('Please Fill All the credentials')

    else:

        usersDB = db.users
        usersList = usersDB.find_one({'username': request.form['username']} and {'password': request.form['password']})
        
        if usersList is not None:
            usersDB = db.users
            userProfile = usersDB.find_one({'username': request.form['username']})
            session['username'] = userProfile['username']
            session['name'] = userProfile['name']
            return home()
        else:
            return('User Not Found')

@app.route('/register', methods=['POST'])
def register():

    if not (request.form['username'] and request.form['password'] and request.form['name'] and
    request.form['email'] and request.form['phone'] and
    request.form['city'] and request.form['occupation']):
        return('Please Fill All the credentials')

    else:

        usersDB = db.users
        usersList = usersDB.find_one({'username': request.form['username']})
        
        if usersList is None:
            userProfile = usersDB.insert_one( { 'username': request.form['username'], 'name': request.form['name'], 
            'password': request.form['password'], 'email': request.form['email'], 'phone': request.form['phone'],
            'city': request.form['city'], 'occupation': request.form['occupation']} )
            # session['username'] = userProfile['username']
            # session['name'] = userProfile['name']
            return home()
        else:
            return('Username Already Exists !')

@app.route('/registrationpage', methods=['GET'])
def registerationpage():
    return render_template('register.html')

@app.route('/changepassword', methods=['POST'])
def changePassword():
    credentialsDB = db.credentials
    credentialsList = credentialsDB.find_one_and_update({'_id': request.form['userid']} , {"$set" : {'password': request.form['password_one']}},
    upsert = False)

    if(credentialsList):
        return ('Password Updated Successfully !')
    else:
        return ('Password Update Failed')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)