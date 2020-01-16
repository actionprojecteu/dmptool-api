import os
import datetime

SECRET_KEY = 'this is the secret key EGG&RIG'
PWD = os.path.abspath(os.curdir)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dbase.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False


PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=24)


MONGO_URI = 'mongodb://localhost:27017/test'

CORS_HEADERS = 'Content-Type'


