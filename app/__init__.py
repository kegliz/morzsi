from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager


db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


def create_app():
  app = Flask(__name__)
  app.config.from_object('config')
  bootstrap.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app


from app import models
