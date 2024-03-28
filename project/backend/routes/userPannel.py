# project/routes/cart_blueprint.py
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from ..models.order import Order
from ..models.product import Product
from ..config.database import db
from ..utils.cartGestion import CartManagement
from ..utils.userGestion import UserManagement  
from ..utils.orderGestion import UserOrder
from sqlalchemy import desc
from flask import jsonify

cart_blueprint = Blueprint('cart', __name__)
user_management = UserManagement()  

@cart_blueprint.route('/userPannel', methods=['GET', 'POST'])
def render_user_pannel():
    username, user = user_management.get_user_info()
    if not user:
        return redirect(url_for('account.login'))
    money = user.Money
    cart_manager = CartManagement(user.UserId)
    user_cart = cart_manager.get_user_cart()
    cart_details = cart_manager.get_cart_details(user_cart)
    user_id = user.UserId
    user_orders = Order.query.filter(Order.UserId == user_id).order_by(desc(Order.OrderDate)).limit(8).all()
    
    orders_details = []
    for order in user_orders:
        product = Product.query.get(order.ProductId)
        if product:
            orders_details.append({
                'product_name': product.Name,
                'quantity': order.Quantity,
                'price': order.Quantity * product.Price,  
                'order_date': order.OrderDate,
                'stock': product.Stock
            })
    
    return render_template('userPannel.html', username=username, money=money, user_cart=cart_details, user_orders=orders_details)


@cart_blueprint.route('/remove_item', methods=['POST'])
def remove_item():
    username, user = user_management.get_user_info()
    if user:
        user_id = user.UserId
        product_id = request.form['product_id']
        print(product_id)
        cart_manager = CartManagement(user_id)
        cart_manager.remove_item_from_cart(product_id)
        # flash('Produit supprimé du panier', 'success')
        return redirect(url_for('cart.render_user_pannel'))
    else:
        flash("Utilisateur non trouvé", 'error')
        return redirect(url_for('login'))
    

@cart_blueprint.route('/load-more-orders', methods=['GET'])
def load_more_orders():
    offset = request.args.get('offset', type=int)
    user_id = user_management.get_user_id()
    user_orders = Order.query.filter(Order.UserId == user_id).order_by(desc(Order.OrderDate)).offset(offset).limit(8).all()
    orders_details = []
    for order in user_orders:
        product = Product.query.get(order.ProductId)
        if product:
            orders_details.append({
                'product_name': product.Name,
                'quantity': order.Quantity,
                'price': order.Quantity * product.Price,  
                'order_date': order.OrderDate
            })
    return jsonify(orders_details)

@cart_blueprint.route('/purchase_from_cart', methods=['POST'])
def purchase_from_cart():
    username, user = user_management.get_user_info()
    if user:
        user_id = user.UserId
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        newOrder = UserOrder(user.UserId, product_id)
        success, error_message, product = newOrder.add_product_to_order(quantity)

        if success :
            cart_manager = CartManagement(user_id)
            cart_manager.delete_item_from_cart(product_id, quantity)
            return redirect(url_for('cart.render_user_pannel'))
        return redirect(url_for('cart.render_user_pannel'))
            
    flash('utilisateur inexistant')
    return redirect(url_for('account.login'))



