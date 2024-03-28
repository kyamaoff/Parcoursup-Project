# project/main.py
from flask import Flask, redirect, render_template
from project.backend.routes.userPannel import cart_blueprint
from project.backend.routes.productsPage import products_blueprint
from project.backend.routes.payementPage import order_blueprint
from project.backend.routes.accountPage import account_blueprint
from project.backend.config.database import init_app

import secrets

app = Flask(__name__)
init_app(app)
app.secret_key = b'\xe2\x80\x93\xb5\xa2\xf5H\x9e\xb1\x8b\x15\x0c\xbc\xf9\xf5'

@app.route('/')
def home():
    return redirect('products')

@app.route('/test')
def test():
    return render_template('navbar.html')

app.register_blueprint(account_blueprint, url_prefix='/auth')    
app.register_blueprint(cart_blueprint, url_prefix='/cart')
app.register_blueprint(products_blueprint, url_prefix='/products')
app.register_blueprint(order_blueprint, url_prefix='/order')

if __name__ == '__main__':
    app.run(debug=True) 