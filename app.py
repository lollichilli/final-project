from flask import redirect, render_template, request, url_for
from config import app, db
from models import User



# primary view
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# transaction view
@app.route('/transactions')
def transaction_history(): 
    return render_template('transaction_history.html')

# send money view
@app.route('/send')
def edit_product(product_id): 
    return render_template('send_money.html') 


if __name__ == '__main__':
    app.run()