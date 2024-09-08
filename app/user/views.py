from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from app.user import user_blueprint
from app.user.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash



@user_blueprint.route('/register',endpoint="register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.html'))

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('user.register'))

        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email address already exists')
            return redirect(url_for('user.register'))

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('user.login'))

    return render_template('user/register.html', form=form)

@user_blueprint.route('/login',endpoint="login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.html'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            print(f"Login attempt: {form.email.data}")
            return redirect(url_for('post.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('user/login.html', form=form)

@user_blueprint.route('/logout',endpoint="logout")
def logout():
    logout_user()
    return redirect(url_for('landing'))
