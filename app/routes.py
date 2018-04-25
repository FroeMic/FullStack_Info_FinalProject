from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import RegistrationForm, LoginForm, SettingsForm, PasswordForm
from app.models import User, Book, Mood, Genre, SearchQuery, Bookmark
from app.utils import dict_to_object, rating_to_stars, ListConverter

# helpers
app.url_map.converters['list'] = ListConverter

# =========================
# Anonymously Accessible 
# =========================

@app.route('/')
def index():
    random_books = Book.get_random()
    for book in random_books:
        print(len(book.moods))
    return render_template('index.html', title='Literapy', explore_books=random_books)

@app.route('/search/<list:moods>', defaults={'genres': []})
@app.route('/search/<list:moods>/<list:genres>')
def search(moods, genres):    
    _moods = Mood.query.filter(Mood.title.in_(moods)).all()
    order = request.args.get('order') if request.args.get('order') else 'score'
    print(order)
    if len(_moods) == 0:
        flash('Oooops! Looks like you we received an empty query.', 'error')
        redirect(url_for('index'))

    _unqueried_moods = Mood.query.filter(~Mood.title.in_(moods)).all()

    _genres = Genre.query.filter(Genre.title.in_(genres)).all()
    _unqueried_genres = Genre.query.filter(~Genre.title.in_(genres)).all()

    query = SearchQuery(_moods, genres=_genres, order_by=order)
    results = query.get_results()

    return render_template('search.html', 
        results=results, 
        rating_to_stars=rating_to_stars, 
        selected_moods=moods, 
        unqueried_moods=_unqueried_moods,
        selected_genres=_genres,
        unqueried_genres=_unqueried_genres,
        sort_order = order )

@app.route('/book/<book_id>')
def show_book(book_id):
    book = Book.query.get(int(book_id))

    bookmarked = False
    if not current_user.is_anonymous:
        check_bookmark  = Bookmark.query.filter_by(book_id=book_id, user_id=current_user.id).first()
        bookmarked = check_bookmark is not None

    if book is None:
        abort(404)

    return render_template('book_details.html', book=book, rating_to_stars=rating_to_stars, title=book.title, bookmarked=bookmarked)

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
@app.route('/bookmark/<book_id>', methods=['GET'])
@login_required
def bookmark(book_id):
    if Bookmark.query.filter_by(user_id=current_user.get_id(), book_id=int(book_id)).first() is None:
        bookmark = Bookmark(user_id=current_user.get_id(), book_id=int(book_id))
        db.session.add(bookmark)
        db.session.commit()

    return redirect(url_for('show_book', book_id=book_id))

@app.route('/bookmark/<book_id>', methods=['DELETE'])
@login_required
def delete_bookmark(book_id):
    bookmark = Bookmark.query.filter_by(user_id=current_user.get_id(), book_id=int(book_id)).first()

    referrer = request.args.get('referrer')
    referrer = referrer if referrer else url_for('mybooks')
    
    redirect_url = url_for('mybooks')
    split_path = referrer.split('/')
    print(referrer)
    print(split_path)
    print(len(split_path))
    print(split_path[-2])
    if len(split_path) >= 2 and split_path[-2] == 'book':
        redirect_url = url_for('show_book', book_id=int(split_path[-1]))

    if bookmark is not None:
        db.session.delete(bookmark)
        db.session.commit()
    return jsonify(
        redirect=True,
        redirect_url=redirect_url
    )

@app.route('/mybooks')
@login_required
def mybooks():
    bookmarks = Bookmark.query.all()
    return render_template('reading_list.html', bookmarks=bookmarks, rating_to_stars=rating_to_stars)

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

@app.route('/settings/password', methods=['GET', 'POST'])
@login_required
def settings_password():
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=int(current_user.id)).first()
        if user is None:
            flash('Error! We could not update your password.', 'error')
            return redirect(url_for('settings_password'))
        if not user.check_password(form.currentpassword.data):
            flash('Error! Your current password appears to be incorrect.', 'error')
            return redirect(url_for('settings_password'))
        user.set_password(form.newpassword.data)
        db.session.commit()
        flash('Your password was updated!', 'info')
        return redirect(url_for('settings_password'))
    return render_template('settings_password.html', title='Settings', form=form)


# =========================
# 3. API
# =========================

@app.route('/api/v1/moods')
def moods():
    moods = [mood.title for mood in Mood.query.all()]
    return jsonify(data = moods, success=True, error=None)
