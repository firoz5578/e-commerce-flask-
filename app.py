from flask import Flask, render_template, session, redirect, url_for, request
from collections import defaultdict
import json
import datetime
import os

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
    return render_template('cart.html', cart_items=cart_items, total=total)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

