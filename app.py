from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime, os, json
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Confirm we're using PostgreSQL (not SQLite fallback)
print ("Using database:", os.getenv("DATABASE_URL"))

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Your existing cart logic...
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Your existing cart logic...



