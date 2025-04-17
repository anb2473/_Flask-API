# Store standard routes for website

from flask import Blueprint, render_template, request, flash, redirect, url_for

from .models import User

from . import db

from flask_login import login_user, login_required, logout_user, current_user

# A hash is a way to secure a password so it isnt in plain text
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['Get', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.form

        email = data.get('email')
        firstName = data.get('firstName')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must have at least 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must have at least 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must have at least 7 characters', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(user, remember=True)

            flash('Account created', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)
