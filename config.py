import os
#from pickle import FALSE

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/data"

SQLALCHEMY_TRACK_MODIFICATIONS = False