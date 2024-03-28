# project/routes/order_blueprint.py
from flask import Blueprint, render_template, request, redirect,  url_for, flash
from ..models.product import Product
from ..models.user import User
from ..utils.userGestion import UserManagement  
from ..utils.orderGestion import UserOrder

order_blueprint = Blueprint('order', __name__)
user_management = UserManagement()  

@order_blueprint.route('/order_summary', methods=['GET', 'POST'])
def get_order_summary():
    product_id = request.args.get('product_id')
    quantity = int(request.args.get('quantity', 1))
    username, user = user_management.get_user_info()
    product = Product.query.get(product_id)
    total_cost= product.Price * quantity

    if total_cost > user.Money :
        return render_template('payement.html', product=product, quantity=quantity, error=True )
    return render_template('payement.html', product=product, quantity=quantity)


@order_blueprint.route('/payment_process', methods=['GET','POST'])
def payment_process():
    product_id = request.form['product_id']  
    quantity = int(request.form['quantity'])
    username, user = user_management.get_user_info()
    if user == False or user is None  :
        return redirect('auth.login')

    newOrder = UserOrder(user.UserId, product_id)
    success, error_message, product = newOrder.add_product_to_order(quantity)
    
    if success:
        # flash("Le produit a été ajouté à votre commande avec succès.", "success")
        return redirect(url_for('cart.render_user_pannel'))
    # else:
    #     flash(error_message, "error")
    
    return redirect(url_for('cart.render_user_pannel'))