# project/models/user.py
from ..config.database import db

class User(db.Model):
    __tablename__ = 'User'
    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text)
    Email = db.Column(db.Text)
    Password = db.Column(db.Text)
    Role = db.Column(db.Text)
    Money = db.Column(db.Float, default=1850)