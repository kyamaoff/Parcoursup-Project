from flask import request, render_template, redirect, url_for, flash
from ..models.user import User
from ..config.database import db
from .signup import bcrypt


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password 

    def authenticate(self):
        user = User.query.filter_by(Name=self.username).first()

        # Check if the user exists in the database
        if user and bcrypt.check_password_hash(user.Password, self.password):
            return True 
        else:
            return False