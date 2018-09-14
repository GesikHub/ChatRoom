from application import db
from application.auth import bp
from application.auth.forms import LoginForm, RegistrationForm
from application.models import User
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.start'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('login/login_error.html', form=form)
        login_user(user, remember=form.remember_me.data)
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.start')
        return redirect(next_page)
    return render_template('login/login.html', form=form)


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.start'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.username.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login.login'))
    return render_template('login/register.html', form=form)


@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.start'))
    else:
        return redirect(url_for('auth.login'))