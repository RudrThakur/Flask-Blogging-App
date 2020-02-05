from celery import Celery
from flask_mail import Message
from mailApp import *
from pymongo import MongoClient
from datetime import datetime

app = Celery('downloaderApp', broker='amqp://localhost//', backend='db+mysql://root@localhost/flaskcelery')

client = MongoClient('mongodb+srv://rudrthakur:rudrcmkt777@rudr-vh5fo.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = client.rudr

#Celery Command
#celery -A downloaderApp worker --pool=solo -l info

@app.task
def logLastLogin(username):
    usersDB = db.users
    lastLoginData = {'username':  username}
    updateLastLogin = { '$set' : {'last_login' : datetime.now()}}
    usersDB.update(lastLoginData, updateLastLogin)

@app.task
def changePassword(username, newPassword):
    usersDB = db.users
    userData = {'username':  username}
    updatePassword = { '$set' : {'password' : newPassword}}
    usersDB.update(userData, updatePassword)

    