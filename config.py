import os
basedir = os.path.abspath(os.path.dirname(__file__))

REFERENCE_NAME = "Morzsi"
#SQLALCHEMY_DATABASE_URI = 'sqlite:///data/test.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/data/test.db')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
