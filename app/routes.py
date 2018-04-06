from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from app import app, db
from app.forms import RegistrationForm
from app.models import User


# =========================
# Anonymously Accessible 
# =========================

@app.route('/')
def index():
    return render_template('index.html', title='Hello World')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, firstname=form.firstname.data, lastname=form.lastname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(user.firstname + ', we successfully registered your account!', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "TODO: Login route not implemented yet"

@app.route('/logout')
def logout():
    return "TODO: Logout route not implemented yet"
