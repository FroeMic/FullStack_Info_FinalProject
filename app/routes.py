from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import RegistrationForm, LoginForm, SettingsForm
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
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# =========================
# 2. Login Required
# # =========================
@app.route('/mybooks')
@login_required
def mybooks():
    return "TODO: Implement the /mybooks route"


@app.route('/settings')
@login_required
def settings():
    return redirect(url_for('settings_profile'))

@app.route('/settings/profile',  methods=['GET', 'POST'])
@login_required
def settings_profile():
    form = SettingsForm(obj=current_user)
    if form.validate_on_submit():
        user = User.query.filter_by(id=int(current_user.id)).first()
        if user is None:
            flash('Error! We could not update your settings.', 'error')
            return redirect(url_for('settings_profile'))

        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.email = form.email.data
        db.session.commit()
        return redirect(url_for('settings_profile'))

    return render_template('settings_profile.html', title='Settings', form=form)

@app.route('/settings/preferences')
@login_required
def settings_preferences():
    return render_template('settings_preferences.html', title='Settings')

@app.route('/settings/password')
@login_required
def settings_password():
    return render_template('settings_password.html', title='Settings')

# =========================
# 3. API
# =========================

@app.route('/api/v1/moods')
def moods():
    moods = [
        'happy',
        'loved',
        'breakup',
        'heartbroken',
        'sad',
        'crazy',
        'excited',
        'thankful',
        'proud',
        'relaxed',
        'awesome',
        'positive',
        'negative',
        'emotional',
        'amused',
        'empty',
        'ill',
        'restless',
        'curious',
        'alone',
        'depressed',
        'tired',
        'entertained',
        'pained',
        'nervous',
        'worried',
        'pumped',
        'optimistic',
        'joyful',
        'motivated',
        'exhausted',
        'nostalgic',
        'in love',
        'lonely',
        'hurt'
    ]
    return jsonify(data = moods, success=True, error=None)