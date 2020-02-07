from pymongo import MongoClient

def databaseUsers():
    return MongoClient('mongodb+srv://rudrthakur:rudrcmkt777@rudr-vh5fo.gcp.mongodb.net/test?retryWrites=true&w=majority').rudr.users

def databasePosts():
    return MongoClient('mongodb+srv://rudrthakur:rudrcmkt777@rudr-vh5fo.gcp.mongodb.net/test?retryWrites=true&w=majority').rudr.posts