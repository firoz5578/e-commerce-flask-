from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime, os, json
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure SQLite or PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///products.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))

# Create the database
with app.app_context():
    db.create_all()

    # Optional: Load from JSON once
    if not Product.query.first():
        with open('products.json') as f:
            product_data = json.load(f)
            for p in product_data:
                db.session.add(Product(
                    id=p['id'],
                    name=p['name'],
                    price=p['price'],
                    description=p['description'],
                    category=p['category']
                ))
            db.session.commit()

# Inject current time to templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

@app.route('/')
def home():
    all_products = Product.query.all()
    categories = defaultdict(list)
    for product in all_products:
        categories[product.category].append(product)
    return render_template('home.html', products=all_products, categories=categories)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    cart_items = Product.query.filter(Product.id.in_(cart_ids)).all()
    total = sum(item.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    return "<h2>Checkout page (to be implemented)</h2>"

if __name__ == '__main__':
    app.run(debug=True)





