# project/utils/orderGestion.py
from ..models.order import Order
from ..models.product import Product
from ..models.user import User
from ..config.database import db
from datetime import datetime

class UserOrder:
    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def add_product_to_order(self, quantity):
        product = Product.query.get(self.product_id)
        if product is None:
            return False, "Produit non trouvé"
        if product.Stock < quantity:
            return False, "Stock insuffisant"
        
        user = User.query.get(self.user_id)
        total_cost = product.Price * quantity
        if user.Money < total_cost:
            return False, "Fonds insuffisants"
        
        order_date = datetime.now().replace(second=0, microsecond=0)
        new_order = Order(UserId=self.user_id, ProductId=self.product_id, Quantity=quantity, OrderDate=order_date)
        db.session.add(new_order)
        product.Stock -= quantity
        user.Money -= total_cost

        db.session.commit()

        return True, None, product