from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sneha1336"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transactions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --------------------- MODELS ---------------------
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    fullname = db.Column(db.String(100))
    balance = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Deposit, Withdraw, Transfer
    amount = db.Column(db.Float, nullable=False)
    to_account = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

# --------------------- ROUTES ---------------------
@app.route('/')
def home():
    return render_template('transaction_home.html')

@app.route('/transactions_home')
def transactions_home():
    return render_template('transaction_home.html')

# ---------- Deposit ----------
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        acc_no = request.form['account_number']
        amount = float(request.form['amount'])

        account = Account.query.filter_by(account_number=acc_no).first()
        if not account:
            flash("❌ Account not found!", "error")
            return redirect(url_for('deposit'))

        account.balance += amount

        txn = Transaction(account_number=acc_no, type="Deposit", amount=amount,
                          description="Money deposited")
        db.session.add(txn)
        db.session.commit()

        flash(f"✅ Deposited ₹{amount} successfully!", "success")
        return redirect(url_for('view_transactions'))

    return render_template('deposit.html')

# ---------- Withdraw ----------
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        acc_no = request.form['account_number']
        amount = float(request.form['amount'])

        account = Account.query.filter_by(account_number=acc_no).first()
        if not account:
            flash("❌ Account not found!", "error")
            return redirect(url_for('withdraw'))

        if account.balance < amount:
            flash("⚠️ Insufficient balance!", "error")
            return redirect(url_for('withdraw'))

        account.balance -= amount
        txn = Transaction(account_number=acc_no, type="Withdraw", amount=amount,
                          description="Money withdrawn")
        db.session.add(txn)
        db.session.commit()

        flash(f"✅ Withdrawn ₹{amount} successfully!", "success")
        return redirect(url_for('view_transactions'))

    return render_template('withdraw.html')

# ---------- Transfer ----------
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        from_acc = request.form['from_account']
        to_acc = request.form['to_account']
        amount = float(request.form['amount'])

        sender = Account.query.filter_by(account_number=from_acc).first()
        receiver = Account.query.filter_by(account_number=to_acc).first()

        if not sender or not receiver:
            flash("❌ Invalid account number(s)!", "error")
            return redirect(url_for('transfer'))

        if sender.balance < amount:
            flash("⚠️ Insufficient balance!", "error")
            return redirect(url_for('transfer'))

        sender.balance -= amount
        receiver.balance += amount

        txn = Transaction(account_number=from_acc, type="Transfer", amount=amount,
                          to_account=to_acc, description="Money transferred")
        db.session.add(txn)
        db.session.commit()

        flash(f"✅ ₹{amount} transferred successfully!", "success")
        return redirect(url_for('view_transactions'))

    return render_template('transfer.html')

# ---------- View Transactions ----------
@app.route('/transactions')
def view_transactions():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return render_template('view_transactions.html', transactions=transactions)

# ---------- Check Balance ----------
@app.route('/balance', methods=['GET', 'POST'])
def check_balance():
    balance = None
    if request.method == 'POST':
        acc_no = request.form['account_number']
        account = Account.query.filter_by(account_number=acc_no).first()
        if account:
            balance = account.balance
        else:
            flash("❌ Account not found!", "error")
    return render_template('check_balance.html', balance=balance)

# ---------- Back to Account Service ----------
@app.route('/home')
def home_redirect():
    return redirect("http://127.0.0.1:5000/account")

# ------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
