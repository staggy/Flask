"""
"""
from website.auth import blueprint

import hashlib
import os
from flask import render_template, request, flash, redirect, url_for
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
import re


# repeatable number/letter combination with a dot or underscore and any number/letter combination
# followed by an @ and domain. not case-sensitive
email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',re.IGNORECASE)

# upper/lower case letter combination, not case-sensitive
first_name_pattern = re.compile(r'^[a-zA-Z]+$', re.IGNORECASE)

# Conditions for a valid password are:
# Should have at least one number.
# Should have at least one uppercase and one lowercase character.
# Should have at least one special symbol.
# Should be between 6 and 20 characters long.
password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email_pattern.match(email):
            flash('Incorrect email/password format. Please try again.', category='error')
        elif not password_pattern.match(password):
            flash('Incorrect email/password format. Please try again.', category='error')

        email = email.lower()
        user = User.authenticate(email, password)
        if not user:
            flash('Incorrect email/password. Please try again.', category='error')
        else:
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('home_blueprint.home'))
    elif request.method == 'GET':
        return render_template("login.html", user=current_user)

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        input_validation = True

        if not email_pattern.match(email):
            flash('Email is not valid. Please check input and try again', category='error')
            input_validation = False
        elif not first_name_pattern.match(first_name):
            flash('Name is not valid. Please check input and try again', category='error')
            input_validation = False
        elif not password_pattern.match(password1):
            flash('Password is not valid. '
                  'Please ensure your password meets all requirements: '
                  'at least one number, '
                  'at least one uppercase and one lowercase character, '
                  'at least one special symbol, '
                  'between 6 to 20 characters long. '
                  'Please check input and try again.', category='error')
            input_validation = False
        elif not password_pattern.match(password2):
            flash('Password is not valid. '
                  'Please ensure your password meets all requirements:\n'
                  'Should have at least one number.\n'
                  'Should have at least one uppercase and one lowercase character.\n'
                  'Should have at least one special symbol.\n'
                  'Should be between 6 to 20 characters long.\n'
                  'Please check input and try again.', category='error')
            input_validation = False
        elif password1 != password2:
            flash('Passwords don\'t match. Please check input and try again.', category='error')
            input_validation = False

        user = User.query.filter_by(email=email).first()
        if user:    # if true user exists
            flash('An account with this email already exists.', category='error')
        elif input_validation == True:
            email = email.lower()   # sets email to all lowercase
            first_name = first_name.capitalize()    # sets first name to proper formatting

            m = hashlib.sha256()    # creates sha256 digester
            m.update(password1.encode('utf-8')) # encodes unicode into bits
            hashed_password = m.digest()
            salt = os.urandom(64)   # generate random bytes for salt
            m.update(salt)
            hashed_and_salted_password = m.digest()

            new_user = User(email=email, first_name=first_name, password=hashed_and_salted_password, salt=salt)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('home_blueprint.home'))
    
    return render_template("register.html", user=current_user)


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@blueprint.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('password1')
        new_password = request.form.get('password2')
        new_password_reentry = request.form.get('password3')
        user = current_user

        msg = hashlib.sha256()
        msg.update(current_password.encode('utf-8'))
        msg.update(user.salt)
        current_hashed_salted_password = msg.digest()

        if not password_pattern.match(current_password) or not password_pattern.match(new_password) \
                or not password_pattern.match(new_password_reentry):
            flash('Incorrect password format. Please try again.', category='error')
        elif current_hashed_salted_password != user.password:
            flash('Incorrect password for this user. Please try again.', category='error')
        elif current_password == new_password:
            flash('New password can not be the same as the current one. Please try again.', category='error')
        elif new_password != new_password_reentry:
            flash('Passwords don\'t match. Please check input and try again.', category='error')
        else:
            m = hashlib.sha256()  # creates sha256 digester
            m.update(new_password.encode('utf-8'))  # encodes unicode into bits
            hashed_password = m.digest()
            salt = os.urandom(64)  # generate random bytes for salt
            m.update(salt)
            hashed_and_salted_password = m.digest()

            user = current_user
            user.password = hashed_and_salted_password
            user.salt = salt

            db.session.commit()

            flash('Password changed! Please log in again.', category='success')
            logout_user()
            return redirect(url_for('auth_blueprint.login'))

    return render_template("changepassword.html", user=current_user)

@blueprint.route('/changeemail', methods=['GET', 'POST'])
@login_required
def change_email():
    if request.method == 'POST':
        new_email = request.form.get('email1')
        user = current_user

        existing_email = User.query.filter_by(email=new_email).first()
        if existing_email:
            flash('An account with this email already exists.', category='error')
        elif not new_email:
            flash('Cannot change email to nothing.', category='error')
        else:
            user.email = new_email

            db.session.commit()

            flash('Email changed! Please log in again.', category='success')
            logout_user()
            return redirect(url_for('auth_blueprint.login'))

    return render_template("changeemail.html", user=current_user)