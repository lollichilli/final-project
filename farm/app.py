from flask import redirect, render_template, request, url_for
from config import app, db
from models import Product, CartItem



# index view
@app.route('/')
def index():
    products = Product.query.filter_by(available=True).all()
    return render_template('index.html', products=products)

# admin view
@app.route('/admin')
def admin():
    products = Product.query.all() 
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
def add_product(): 
    if request.method == 'POST': 
        product = Product(name=request.form['name'], description=request.form['description'], price=request.form['price'], image=request.form['image'])
        db.session.add(product)
        db.session.commit() 
        return redirect(url_for('admin'))
    return render_template('add_product.html')

@app.route('/admin/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id): 
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST': 
        product.name = request.form['name'] 
        product.description = request.form['description'] 
        product.price = request.form['price']  
        db.session.commit() 
        return redirect(url_for('admin')) 
    return render_template('edit_product.html', product=product) 

@app.route('/admin/<int:product_id>/delete') 
def delete_product(product_id): 
    product = Product.query.get_or_404(product_id) 
    db.session.delete(product) 
    db.session.commit() 
    return redirect(url_for('admin')) 


# Cart View
@app.route('/cart') 
def cart(): 
    items = db.session.query(CartItem, Product).join(Product).all() 
    return render_template('cart.html', items=items) 

@app.route('/cart/add/<int:product_id>') 
def add_to_cart(product_id): 
    cart_item = CartItem(product_id=product_id) 
    db.session.add(cart_item) 
    db.session.commit() 
    return redirect(url_for('index'))
 
@app.route('/cart/<int:item_id>/delete') 
def remove_from_cart(item_id): 
    item = CartItem.query.get_or_404(item_id) 
    db.session.delete(item) 
    db.session.commit() 
    return redirect(url_for('cart')) 



if __name__ == '__main__':
    app.run()