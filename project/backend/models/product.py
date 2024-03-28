# project/models/product.py
from ..config.database import db

class Product(db.Model):
    __tablename__ = 'Product'
    ProductId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text)
    Description = db.Column(db.Text)
    Image = db.Column(db.Text)
    Price = db.Column(db.Float)
    Stock = db.Column(db.Integer)