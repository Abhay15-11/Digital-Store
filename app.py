from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Yeh line database ko direct current/same folder me 'store.db' ke naam se save karegi
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model (Product Table)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    whatsapp_no = db.Column(db.String(20), nullable=False)

# Database create karne ke liye
with app.app_context():
    db.create_all()

# 1. Main Store Page (Frontend)
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# 2. Add Product Page (Admin Panel)
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        price = int(request.form['price'])
        image = request.form['image']
        whatsapp_no = request.form['whatsapp_no']

        new_product = Product(
            name=name,
            category=category,
            description=description,
            price=price,
            image=image,
            whatsapp_no=whatsapp_no
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = int(os.environ.get('PORT',5000)))
