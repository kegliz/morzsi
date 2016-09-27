from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.getTestUser()
  #    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
#    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @staticmethod
    def getTestUser():
      return User(email='john@example.com', username='john', password='cat', id=0)

    @property
    def password(self):
      raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
      self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
      return check_password_hash(self.password_hash, password)


class Kedves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    birth_ordinal = db.Column(db.Integer, nullable=False)

#    def __init__(self, name, birth_ordinal):
#        self.name = name
#        self.birth_ordinal = birth_ordinal

    def __repr__(self):
        return '<Kedves {} {}>'.format(self.name, datetime.date.fromordinal(self.birth_ordinal))

    def birth_date(self):
        return datetime.date.fromordinal(self.birth_ordinal)

    def days_diff(self, ref, year):
        offset = self.birth_date()
        return datetime.date(int(year), offset.month, offset.day).toordinal()-ref.birth_ordinal


