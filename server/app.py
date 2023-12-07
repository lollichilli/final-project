#!/usr/bin/env python3
"""
banking api
"""

import json
from flask import Response
from config import app, db
from models import User, Account, Transaction
from datetime import datetime

# Admin route to see all users/info
@app.route("/api/v1/banking/admin")
def send_admin() :
    resp = Response(json.dumps({"All Users": get_admin()}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

# Register new user with initial deposit
@app.route("/api/v1/banking/register/<username>/<email>/<password>/<amount>")
def send_user_registration_i(username, email, password, amount) :
    resp = Response(json.dumps({"Success": get_user_registration_i(username, email, password, amount)}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

# Register new user with balance 0
@app.route("/api/v1/banking/register/<username>/<email>/<password>")
def send_user_registration(username, email, password) :
    resp = Response(json.dumps({"Success": get_user_registration(username, email, password)}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

# User info
@app.route("/api/v1/banking/<username>")
def send_user_info(username) :
    resp = Response(json.dumps({f"{username}": get_info(username)}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

# User balance
@app.route("/api/v1/banking/<username>/balance")
def send_balance(username) :
    resp = Response(json.dumps({"Balance": get_balance(username)}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

# User transactions (to)
@app.route("/api/v1/banking/<username>/transactionst")
def send_transactions_t(username) :
    resp = Response(json.dumps({"Transactions_t": get_transactions_t(username)}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

# User transactions (from)
@app.route("/api/v1/banking/<username>/transactionsf")
def send_transactions_f(username) :
    resp = Response(json.dumps({"Transactions_f": get_transactions_f(username)}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

# User sends money to other user
@app.route("/api/v1/banking/<username>/send/<otherUsername>/<amount>")
def send_money(username, otherUsername, amount) :
    resp = Response(json.dumps({"Success": get_money(username, otherUsername, amount)}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Content-Type"] = "application/json"
    return resp

def get_admin() :
    """Return a all user info"""
    try:
        all_users = User.query.all()
        print(all_users)
        users = []
        for user in all_users :
            user_info = []
            user_info.append(user.user_name)
            user_info.append(user.user_email)
            user_info.append(user.user_password)
            users.append(user_info)
        return users
    except Exception as e:
        print(e)
        return e

def get_user_registration_i(username, email, password, amount) :
    """Return true/false and msg based on success of registration"""
    try:
        user_check = User.query.filter_by(user_name=username).first()
        email_check = User.query.filter_by(user_email=email).first()
        if (user_check and email_check) :
            return [False, "User Already Exist"]
        elif (user_check) :
            return [False, "Username Already Exists"]
        elif (email_check) :
            return [False, "Email Already Exists"]
        else :
            # Create a new user
            newUser = User(
                user_name = username,
                user_email = email,
                user_password = password
            )
            # Add the new user to the database
            db.session.add(newUser)
            db.session.commit()
            # Initialize the account balance
            newAccount = Account(
                u_id = newUser.user_id,
                account_balance = float(amount)
            )
            db.session.add(newAccount)
            db.session.commit()

            return [True]
    except Exception as e:
        print(e)
        return e
    
def get_user_registration(username, email, password) :
    """Return true/false and msg based on success of registration"""
    try:
        user_check = User.query.filter_by(user_name=username).first()
        email_check = User.query.filter_by(user_email=email).first()
        if (user_check and email_check) :
            return [False, "User Already Exist"]
        elif (user_check) :
            return [False, "Username Already Exists"]
        elif (email_check) :
            return [False, "Email Already Exists"]
        else :
            # Create a new user
            newUser = User(
                user_name = username,
                user_email = email,
                user_password = password
            )
            # Add the new user to the database
            db.session.add(newUser)
            db.session.commit()
            # Initialize the account balance
            newAccount = Account(
                u_id = newUser.user_id,
                account_balance = 0
            )
            db.session.add(newAccount)
            db.session.commit()

            return [True]
    except Exception as e:
        print(e)
        return e

def get_info(username) :
    """Return user info"""
    try:
        user = User.query.filter_by(user_name=username).first()
        return [user.user_id, user.user_name, user.user_email, user.user_password]
    except Exception as e:
        print(e)
        return e

def get_balance(username) :
    """Return balance"""
    try:
        user = User.query.filter_by(user_name=username).first()
        user_id = user.user_id
        account = Account.query.filter_by(u_id=user_id).first()
        balance = account.account_balance
        return balance
    except Exception as e:
        print(e)
        return e
    
def get_transactions_t(username) :
    """Return transactions sent to user"""
    try:
        user = User.query.filter_by(user_name=username).first()
        user_id = user.user_id
        account = Account.query.filter_by(u_id=user_id).first()
        account_id = account.account_id
        transactions_to_user = Transaction.query.filter_by(to_account_id=account_id).order_by(Transaction.transaction_date)
        transactions_to_user_list = []
        for transaction in transactions_to_user :

            # Get the usernames
            from_account = Account.query.filter_by(account_id=transaction.from_account_id).first()
            to_account = Account.query.filter_by(account_id=transaction.to_account_id).first()
            from_account_u = User.query.filter_by(user_id=from_account.u_id).first()
            to_account_u = User.query.filter_by(user_id=to_account.u_id).first()
            from_account_u_name = from_account_u.user_name
            to_account_u_name = to_account_u.user_name

            transaction_components_list = [
                transaction.transaction_id,
                str(transaction.transaction_date),
                from_account_u_name,
                to_account_u_name,
                transaction.amount
                ]
            transactions_to_user_list.append(transaction_components_list)

        return transactions_to_user_list
    except Exception as e:
        print(e)
        return e
    
def get_transactions_f(username) :
    """Return transactions sent from user"""
    try:
        user = User.query.filter_by(user_name=username).first()
        user_id = user.user_id
        account = Account.query.filter_by(u_id=user_id).first()
        account_id = account.account_id
        transactions_from_user = Transaction.query.filter_by(from_account_id=account_id).order_by(Transaction.transaction_date)
        transactions_from_user_list = []
        for transaction in transactions_from_user :

            # Get the usernames
            from_account = Account.query.filter_by(account_id=transaction.from_account_id).first()
            to_account = Account.query.filter_by(account_id=transaction.to_account_id).first()
            from_account_u = User.query.filter_by(user_id=from_account.u_id).first()
            to_account_u = User.query.filter_by(user_id=to_account.u_id).first()
            from_account_u_name = from_account_u.user_name
            to_account_u_name = to_account_u.user_name

            transaction_components_list = [
                transaction.transaction_id,
                str(transaction.transaction_date),
                from_account_u_name,
                to_account_u_name,
                transaction.amount
                ]
            transactions_from_user_list.append(transaction_components_list)

        return transactions_from_user_list
    except Exception as e:
        print(e)
        return e
    
def get_money(username, otherUsername, amount) :
    """Return true/false based on success of sending money to otherUsername from username's account"""
    try:
        # Get the from account
        from_user = User.query.filter_by(user_name=username).first()
        from_account = Account.query.filter_by(u_id=from_user.user_id).first()

        # Get the to account
        to_user = User.query.filter_by(user_name=otherUsername).first()

        # Return false if the to account does not exist
        if (not to_user) :
            return [False, "You are trying to send to a nonexistant account"]
        
        to_account = Account.query.filter_by(u_id=to_user.user_id).first()

        # Return false if the from account has insufficient funds
        if (float(from_account.account_balance) < float(amount)) :
            return [False, "You are trying to send more than what you have"]



        # Send the money
        from_account_new_balance = from_account.account_balance - float(amount)
        to_account_new_balance = to_account.account_balance + float(amount)
        from_account.account_balance = from_account_new_balance
        db.session.commit()
        to_account.account_balance = to_account_new_balance
        db.session.commit()

        # Record the transaction
        newTransaction = Transaction(
            transaction_date = datetime.now(),
            from_account_id = from_account.account_id,
            to_account_id = to_account.account_id,
            amount = amount
        )

        # Add the transaction to database
        db.session.add(newTransaction)
        db.session.commit()

        return [True]

    except Exception as e:
        print(e)
        return e



if (__name__ == "__main__") :
    app.run(debug=True)