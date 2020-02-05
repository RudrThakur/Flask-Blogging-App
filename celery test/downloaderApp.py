from celery import Celery

app = Celery('downloaderApp', broker='amqp://localhost//', backend='db+mysql://root@localhost/flaskcelery')

#Celery Command
#celery -A downloaderApp worker --pool=solo -l info

@app.task
def reverse(string):
    return string[::-1]