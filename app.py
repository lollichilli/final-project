from flask import redirect, render_template, request, url_for, session
from config import app, db
from models import User, Account, Transaction

# Home Page
@app.route('/')
def index():
    # Check if the user is already in session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else :
        # Get the user id from session
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        username = user.user_name
        return render_template('index.html', user_id=user_id, user_name=username)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the login info from the form and query it from User
        loginForm = request.form
        username = loginForm['username']
        password = loginForm['password']
        currentUser = User.query.filter_by(user_name=username).first()
        # Check if valid and then redirect user accordingly
        if (currentUser) :
            if (currentUser.user_password == password) :
                session['user_id'] = currentUser.user_id
                return redirect(url_for('index'))
            else :
                return "Incorrect Password"
        else :
            return "Invalid Login"
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the registration form info
        registrationForm = request.form
        # Check if the user already exists
        user = User.query.filter_by(user_name=registrationForm['username']).first()
        if (user) :
            return "User Already Exists"
        else :
            # Create a new user
            newUser = User(
                user_name = registrationForm['username'],
                user_email = registrationForm['email'],
                user_password = registrationForm['password']
            )
            # Add the new user to the database
            db.session.add(newUser)
            db.session.commit()
            # Store the user in session
            session['user_id'] = newUser.user_id
            # Redirect to the home page with the user parameter updated
            return redirect(url_for('index'))
    return render_template('register.html')

# Transaction view
@app.route('/transactions', methods=['POST'])
def transaction_history():
    # Verify that user is logged in
    if 'user_id' not in session:
        return redirect(url_for('index', user=None))
    # Get the user id from session
    user_id = session['user_id']
    # Get the users transactions from the user
    transactions_from_user = Transaction.query.filter_by(from_account_id=user_id).all().order_by(Transaction.transaction_date).desc()
    # Get the transactions to the user
    transactions_to_user = Transaction.query.filter_by(to_account_id=user_id).all().order_by(Transaction.transaction_date).desc()
    # Render the template with the users transaction history
    return render_template(
        'transaction_history.html',
        transactions_from_user=transactions_from_user,
        transactions_to_user=transactions_to_user
        )

if __name__ == '__main__':
    app.run()