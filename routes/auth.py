from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, Parent

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        parent = Parent.query.filter_by(email=email).first()

        if not parent or not check_password_hash(parent.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(parent, remember=remember)
        return redirect(url_for('dashboard.index'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        phone = request.form.get('phone')

        user = Parent.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        new_parent = Parent(
            email=email, 
            name=name, 
            password_hash=generate_password_hash(password, method='sha256'),
            phone=phone
        )

        db.session.add(new_parent)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
