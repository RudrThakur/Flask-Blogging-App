from celery import Celery
from pymongo import MongoClient
from datetime import datetime
from db import *

app = Celery('taskworker', broker='amqp://localhost//', backend='db+mysql://root@localhost/flaskcelery')
#Celery Command
#celery -A taskworker worker --pool=solo -l info

@app.task
def logLastLogin(username):
    usersDB = databaseUsers()
    lastLoginData = {'username':  username}
    updateLastLogin = { '$set' : {'last_login' : datetime.now()}}
    usersDB.update(lastLoginData, updateLastLogin)