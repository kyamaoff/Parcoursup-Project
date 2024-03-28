# backend/auth/accountPage.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from project.backend.auth.login import Login
from project.backend.auth.signup import Signup
import secrets

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_data = Login(username=request.form['username'], password=request.form['password'])
        if login_data.authenticate() == True:
            session['username'] = request.form['username']
            # Generate token session
            session['user_token'] = secrets.token_urlsafe(16)
            flash('Login successful', 'success')
            return redirect(url_for('cart.render_user_pannel'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    return render_template('login.html')

@account_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    errors = {}
    if request.method == 'POST':
        signup_data = Signup(
            username=request.form['newUsername'],
            email=request.form['newEmail'],
            password=request.form['newPassword']
        )

        email_error = signup_data.invalid_mail()
        password_errors = signup_data.invalid_password()
        username_errors = signup_data.invalid_username()

        if email_error:
            errors['email'] = email_error
        if password_errors:
            errors['password'] = password_errors
        if username_errors:
            errors['username'] = username_errors

        if not errors:
            signup_data.create_account()
            flash('Compte créé avec succès', 'success')  
            return redirect(url_for('account.login'))  

    return render_template('register.html', errors=errors)


@account_blueprint.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop("username", None)
    flash('Vous avez été déconnecté', 'success')
    response = redirect(url_for('account.login')) 

    return response