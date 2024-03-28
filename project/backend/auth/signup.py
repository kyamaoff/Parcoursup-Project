from flask import request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from ..models.user import User
from ..config.database import db
import re

bcrypt = Bcrypt()

class Signup:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email 
        self.password = password

    def invalid_mail(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            return 'L\'adresse mail n\'est pas valide.'
        return None
    
    def invalid_password(self):
        error_messages = []
        if len(self.password) < 8:
            error_messages.append('8 caractères')
        if not re.search(r'\d', self.password):
            error_messages.append('un chiffre')
        if not any(c.isupper() for c in self.password):
            error_messages.append('une majuscule')
        if error_messages:
            return ' + '.join(error_messages) + ' requis'
        return None
    
    def invalid_username(self):
        error_messages = []
        if len(self.username) < 3 or len(self.username) > 16:
            error_messages.append('Entre  3 et 16 caractères')
        if ' ' in self.username:
            error_messages.append('Le pseudo ne doit pas contenir d\'espace')
        existing_user = User.query.filter_by(Name=self.username).first()
        if existing_user:
            error_messages.append('Le pseudo est déjà utilisé')
        return error_messages if error_messages else None

    def create_account(self):
        hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        new_user = User(Name=self.username, Email=self.email, Password=hashed_password, Role='user', Money=1850.0)
        db.session.add(new_user)
        db.session.commit()
        return True