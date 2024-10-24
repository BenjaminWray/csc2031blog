from flask import Blueprint, render_template, flash, redirect, url_for, session, get_flashed_messages
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy.session import Session
from flask_wtf import FlaskForm
from sqlalchemy import false
from markupsafe import Markup
import pyotp
from wtforms.validators import NoneOf

from accounts.forms import RegistrationForm, LoginForm
from config import User, db, limiter

accounts_bp = Blueprint('accounts', __name__, template_folder='templates')
max_login_attempts = 3



@accounts_bp.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', category="danger")
            return render_template('accounts/registration.html', form=form)

        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account Created. You have to enable Multi-Factor Authentication first to login', category='success')
        return render_template('accounts/mfasetup.html', secret=new_user.mfakey, uri=new_user.uri())

    return render_template('accounts/registration.html', form=form)

@accounts_bp.route('/login', methods=['GET','POST'])
@limiter.limit("20 per minute")
def login():
    form = LoginForm()

    if not "login_attempts" in session:
        session["login_attempts"] = 0

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.verify_password(form.password.data):
                session["login_attempts"] = 0
                if user.verify_otp(form.otp.data):
                    if not user.mfaenabled:
                        user.mfaenabled = True
                        db.session.commit()
                    login_user(user)
                    flash('Login Successful', category='success')
                    return redirect(url_for('posts.posts'))
                if not user.mfaenabled:
                    flash('MFA is not enabled. You have to enable Multi-Factor Authentication first to login', category='danger')
                    return render_template('accounts/mfasetup.html', secret=user.mfakey, uri=user.uri())


        session['login_attempts'] += 1

        if session['login_attempts'] >= max_login_attempts:
            flash(Markup('You have tried to log in too many times. Please click <a href="\\unlock">here</a> to unlock account.'), category='danger')
            return render_template('accounts/login.html')

        flash('Invalid Credentials. You have ' + str(max_login_attempts - session.get('login_attempts')) + ' attempt(s) remaining.', category="danger")
        return redirect(url_for('accounts.login'))

    return render_template('accounts/login.html', form=form)


@accounts_bp.route('/account')
def account():
    return render_template('accounts/account.html', user=current_user)

@accounts_bp.route('/unlock')
def unlock():
    session["login_attempts"] = 0
    return redirect(url_for('accounts.login'))

@accounts_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))