from celery import Celery
from pymongo import MongoClient
from datetime import datetime
import db

app = Celery('taskworker', broker='amqp://localhost//', backend='db+mysql://root@localhost/flaskcelery')
#Celery Command
#celery -A downloaderApp worker --pool=solo -l info

@app.task
def logLastLogin(username):
    usersDB = db.users
    lastLoginData = {'username':  username}
    updateLastLogin = { '$set' : {'last_login' : datetime.now()}}
    usersDB.update(lastLoginData, updateLastLogin)