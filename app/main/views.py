from flask import render_template, flash, redirect, session, url_for, request, current_app
from app import db
from app.forms import KedvesForm, ReferenceForm
from app.models import Kedves
import datetime
from flask.ext.login import login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm
from . import main


@main.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
#      user = User.getTestUser()
#      login_user(user, form.remember_me.data)
#      return redirect(request.args.get('next') or url_for('.index'))


     user = User.query.filter_by(email=form.email.data).first()
     if user is not None and user.verify_password(form.password.data):
         login_user(user, form.remember_me.data)
         return redirect(request.args.get('next') or url_for('.index'))
     flash('Invalid username or password.')
  return render_template('login.html',
                         title='Login',
                         form=form)
                         
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.index'))

@main.route('/')
@main.route('/index')
@login_required
def index():
  year = session.get('reference_year')
  if year is None:
    year = datetime.date.today().year # default
  ref_id = session.get('reference_id')
  if ref_id is None:
    ref = Kedves.query.filter_by(name=current_app.config['REFERENCE_NAME']).first() # default
  else:
    ref = Kedves.query.get(ref_id)
  kedves_list=Kedves.query.all()
  return render_template('index.html',
                           kedves_list=kedves_list,
                           year=year,
                           ref=ref)

@main.route('/reference', methods=['GET', 'POST'])
@login_required
def reference():
  form = ReferenceForm()
  form.reference_id.choices=[(k.id, k.name) for k in Kedves.query.all()]
  if form.validate_on_submit():
    session['reference_id'] = form.reference_id.data
    session['reference_year'] = form.year.data
    return redirect(url_for('.index'))
  return render_template('reference.html',
                         title='Reference',
                         form=form)

@main.route('/create_kedves', methods=['GET', 'POST'])
@login_required
def create_kedves():
  form = KedvesForm()
  if form.validate_on_submit():
    name = form.name.data
    birth_ordinal = form.birth_date.data.toordinal()
    kedves = Kedves (name=name, birth_ordinal=birth_ordinal)
    db.session.add(kedves)
    db.session.commit()
    flash("New kedves '{}' was successfully added".format(name))
    return redirect(url_for('.index'))
  return render_template('create_kedves.html',
                         title='Create',
                         form=form)

@main.route('/delete_kedves/<id>', methods=['POST', 'GET'])
@login_required
def delete_kedves(id):
  kedves = Kedves.query.get(id)
  db.session.delete(kedves)
  db.session.commit()
  flash('deleted')
  return redirect(url_for('.index'))

@main.route('/edit_kedves/<id>', methods=['POST', 'GET'])
@login_required
def edit_kedves(id):
  form = KedvesForm()
  kedves = Kedves.query.get(id)
  if form.validate_on_submit():
    kedves.name = form.name.data
    kedves.birth_ordinal = form.birth_date.data.toordinal()
    db.session.commit()
    flash('modified')
    return redirect(url_for('.index'))
  return render_template('edit_kedves.html',
                         form=form,
                         title='Edit',
                         kedves=kedves)






