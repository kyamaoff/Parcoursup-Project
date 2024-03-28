from flask import Blueprint, render_template, flash, session, request, redirect, url_for
from ..utils.cartGestion import CartManagement
from ..utils.userGestion import UserManagement
from ..models.product import Product
from ..models.cart import Cart

products_blueprint = Blueprint('products', __name__)
user_management = UserManagement()

@products_blueprint.route('/', methods=['GET', 'POST'])
def render_product_page():
    products = Product.query.all()  
    username, user = user_management.get_user_info()
    for product in products:
        if product.Stock > 10:
            product.stock_status = 'En Stock'
        elif 0 < product.Stock <= 10:
            product.stock_status = f'Il reste {product.Stock} produit(s)'
        else:
            product.stock_status = 'Indisponible'
        notification = session.pop('notification', None)
    if user : 
        return render_template('products.html', products=products, connected=bool(user), notification=notification)
    else :
        return render_template('products.html', products=products, connected=bool(user), notification=notification)
    

@products_blueprint.route('/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.query.get(product_id)
    username, user = user_management.get_user_info()
    notification = session.pop('notification', None)
    if product.Stock > 10:
        stock_status = 'En stock'
    elif 0 < product.Stock <= 10:
        stock_status = f'Il reste {product.Stock} produit(s)'
    else:
        stock_status = 'Indisponible'
        return render_template('product_detail_sold_out.html', product=product, product_id=product_id, stock_status=stock_status, connected=bool(user), notification=notification)
    if user :
        return render_template('product_detail.html', product=product, product_id=product_id, stock_status=stock_status, connected=bool(user), notification=notification)
    else :
        return render_template('product_detail.html', product=product, product_id=product_id, stock_status=stock_status, connected=bool(user), notification=notification)
        

@products_blueprint.route('/add_item_to_cart', methods=['POST'])
def add_item_to_cart():
    username, user = user_management.get_user_info()
    if user:
        cart_manager = CartManagement(user.UserId)
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))
        cart_manager.add_item_to_cart(product_id, quantity)
        return redirect(url_for('cart.render_user_pannel', product_id=product_id))
    else:
        return redirect(url_for('account.login'))
    

@products_blueprint.route('/purchase_item', methods=['POST'])
def purchase():
    username, user = user_management.get_user_info()
    if user:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))
        product = Product.query.get(product_id)
        return redirect(url_for('order.get_order_summary', product_id=product_id, quantity=quantity)) 
    else:
        return redirect(url_for('account.login'))
