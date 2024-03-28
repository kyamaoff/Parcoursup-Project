from flask import flash, session
from ..models.cart import Cart
from ..models.product import Product
from ..config.database import db

class CartManagement:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_cart(self):
        return Cart.query.filter_by(UserId=self.user_id).all()

    def get_cart_details(self, cart):
        cart_details = []
        for item in cart:
            product = Product.query.get(item.ProductId)
            if product:
                stock_status = self.get_stock_status(product.Stock)
                product_details = {
                    'cart_id': item.CartId,
                    'quantity': item.Quantity,
                    'product_id': product.ProductId,
                    'product_name': product.Name,
                    'product_price': product.Price,
                    'product_image': product.Image,
                    'product_quantity': product.Stock,
                    'stock_status': stock_status
                }
                cart_details.append(product_details)
        return cart_details

    def remove_item_from_cart(self, product_id):
        cart_item = Cart.query.filter_by(UserId=self.user_id, ProductId=product_id).first()
        if cart_item:
            if cart_item.Quantity > 1:
                cart_item.Quantity -= 1
            else:
                db.session.delete(cart_item)
            db.session.commit()
        #     flash('Produit supprimé du panier', 'success')
        # else:
        #     flash('Produit introuvable dans le panier', 'error')
            
    def delete_item_from_cart(self, product_id, quantity):
        for i in range(quantity):
            self.remove_item_from_cart(product_id)

    def add_item_to_cart(self, product_id, quantity):
        product = Product.query.get(product_id)
        if product:
            if product.Stock >= quantity:
                existing_cart_item = Cart.query.filter_by(UserId=self.user_id, ProductId=product_id).first()
                if existing_cart_item:
                    existing_cart_item.Quantity += quantity
                else:
                    new_cart_item = Cart(UserId=self.user_id, ProductId=product_id, Quantity=quantity)
                    db.session.add(new_cart_item)
                db.session.commit()
                # Nous enregistrons la notification dans la session
                session['notification'] = {'message': 'Produit ajouté au panier', 'type': 'success'}
            else:
                session['notification'] = {'message': 'Quantité demandée indisponible en stock', 'type': 'error'}
        else:
            session['notification'] = {'message': 'Produit introuvable', 'type': 'error'}
    
    def get_stock_status(self, stock):
        if stock > 10:
            return 'En stock'
        elif 0 < stock <= 10:
            return f'Il reste {stock} produit(s)'
        else:
            return 'Indisponible'