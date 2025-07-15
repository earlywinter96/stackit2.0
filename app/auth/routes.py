from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
from app.extensions import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
