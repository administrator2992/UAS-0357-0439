import os
#from pickle import FALSE

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'log.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False