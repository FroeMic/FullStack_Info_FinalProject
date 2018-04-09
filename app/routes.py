from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import RegistrationForm, LoginForm, SettingsForm
from app.models import User
from app.utils import dict_to_object, rating_to_stars


# =========================
# Anonymously Accessible 
# =========================

@app.route('/')
def index():
    return render_template('index.html', title='App Name')

@app.route('/search')
def search():
    mood = request.args.get('mood')

    results = [
        dict_to_object({
            'id': 1,
            'isbn': '0770430074',
            'isbn13': '9780770430078',
            'title': 'Life of Pi',
            'author': 'Yann Martel',
            'price': 9.99,
            'rating': 3.86,
            'excerpt': 'Life of Pi is a fantasy adventure novel by Yann Martel published in 2001. The protagonist, Piscine Molitor "Pi" Patel, a Tamil boy from Pondicherry, explores issues of spirituality and practicality from an early age. He survives 227 days after a shipwreck while stranded on a boat in the Pacific Ocean with a Bengal tiger named Richard Parker.' ,
            'match': 0.96,
            'image_url': 'https://images.gr-assets.com/books/1320562005l/4214.jpg',
            'genres': [
                'Fantasy',
                'Adventure',
                'Classics', 
                'Contemporary',
                'Fiction',
                'Literature',
                'Philosophy'
            ]
        }),
        dict_to_object({
            'id': 17,
            'isbn': '0770430074',
            'isbn13': '9780770430078',
            'title': 'Homo Deus: A Brief History of Tomorrow',
            'author': 'Yuval Noah Harari',
            'price': 17.99,
            'rating': 4.38,
            'excerpt': 'Yuval Noah Harari, author of the critically-acclaimed New York Times bestseller and international phenomenon Sapiens, returns with an equally original, compelling, and provocative book, turning his focus toward humanity’s future, and our quest to upgrade humans into gods. Over the past century humankind has managed to do the impossible and rein in famine, plague, and war. This may seem hard to accept, but, as Harari explains in his trademark style—thorough, yet riveting—famine, plague and war have been transformed from incomprehensible and uncontrollable forces of nature into manageable challenges. For the first time ever, more people die from eating too much than from eating too little; more people die from old age than from infectious diseases; and more people commit suicide than are killed by soldiers, terrorists and criminals put together. The average American is a thousand times more likely to die from binging at McDonalds than from being blown up by Al Qaeda. What then will replace famine, plague, and war at the top of the human agenda? As the self-made gods of planet earth, what destinies will we set ourselves, and which quests will we undertake? Homo Deus explores the projects, dreams and nightmares that will shape the twenty-first century—from overcoming death to creating artificial life. It asks the fundamental questions: Where do we go from here? And how will we protect this fragile world from our own destructive powers? This is the next stage of evolution. This is Homo Deus. With the same insight and clarity that made Sapiens an international hit and a New York Times bestseller, Harari maps out our future.',
            'match': 0.76,
            'image_url': 'https://images.gr-assets.com/books/1522691489l/39704901.jpg',
            'genres': [
                'Nonfiction',
                'Science',
                'History', 
                'Philosophy',
                'Anthropology',
            ]
        }),
    ]

    return render_template('search.html', results=results, rating_to_stars=rating_to_stars, mood=mood)


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