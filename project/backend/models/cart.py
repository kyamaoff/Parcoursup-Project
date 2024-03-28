# project/models/cart.py
from ..config.database import db

class Cart(db.Model):
    __tablename__ = 'Cart'
    CartId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    ProductId = db.Column(db.Integer, db.ForeignKey('Product.ProductId'), nullable=False)
    Quantity = db.Column(db.Integer)

    user = db.relationship('User', backref='cart')
    product = db.relationship('Product', backref='cart')    