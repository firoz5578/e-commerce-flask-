from flask import Flask, render_template, session, redirect, url_for, request
from collections import defaultdict
import json
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open('products.json') as f:
    products = json.load(f)

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow}

@app.route('/')
def home():
    categories = defaultdict(list)
    for product in products:
        categories[product['category']].append(product)
    return render_template('home.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product)
    session.modified = True
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
