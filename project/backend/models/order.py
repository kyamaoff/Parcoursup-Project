# project/models/order.py
from ..config.database import db

class Order(db.Model):
    __tablename__ = 'Order'
    OrderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId'), nullable=False)
    ProductId = db.Column(db.Integer, db.ForeignKey('Product.ProductId'), nullable=False)
    Quantity = db.Column(db.Integer)
    OrderDate = db.Column(db.Text)
    is_paid = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')