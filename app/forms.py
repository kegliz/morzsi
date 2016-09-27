from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, SelectField, DateField, SubmitField, PasswordField, BooleanField
#from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length, Regexp, Required, EqualTo
from .models import User
from wtforms import ValidationError

class LoginForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ReferenceForm(Form):
    year = IntegerField('year', validators=[InputRequired()])
    reference_id = SelectField('reference', coerce=int)

class KedvesForm(Form):
    name = StringField('name', validators=[InputRequired()])
    birth_date = DateField('birth_date', validators=[InputRequired()])
