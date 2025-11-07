from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sneha1336"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ------------------------------
# DATABASE MODEL
# ------------------------------
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20))
    branch = db.Column(db.String(100))
    ifsc = db.Column(db.String(20))
    pin = db.Column(db.String(10), nullable=False)

with app.app_context():
    db.create_all()

# ------------------------------
# ROUTES
# ------------------------------
@app.route("/")
def account_home():
    return render_template("account.html")

@app.route("/add_account", methods=["GET", "POST"])
def add_account():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        address = request.form["address"]
        account_type = request.form["account_type"]
        branch = request.form["branch"]
        ifsc = request.form["ifsc"]
        pin = request.form["pin"]

        # ✅ Generate account number sequentially
        last_acc = Account.query.order_by(Account.id.desc()).first()
        if last_acc:
            account_number = str(int(last_acc.account_number) + 1)
        else:
            account_number = "202500001"

        # Prevent duplicate username
        if Account.query.filter_by(username=username).first():
            flash("❌ Username already exists!", "error")
            return redirect(url_for("add_account"))

        new_account = Account(
            fullname=fullname,
            username=username,
            email=email,
            phone=phone,
            dob=dob,
            gender=gender,
            address=address,
            account_number=account_number,
            account_type=account_type,
            branch=branch,
            ifsc=ifsc,
            pin=pin
        )

        db.session.add(new_account)
        db.session.commit()
        flash(f"✅ Account created successfully! Account Number: {account_number}", "success")
        return redirect(url_for("view_accounts"))
    
    return render_template("add_account.html")

@app.route('/account')
def account():
    return render_template("account.html")


@app.route("/view_accounts")
def view_accounts():
    accounts = Account.query.all()
    return render_template("view_accounts.html", accounts=accounts)

# ------------------------------
# EDIT ACCOUNT
# ------------------------------
@app.route("/edit_account/<int:id>", methods=["GET", "POST"])
def edit_account(id):
    account = Account.query.get_or_404(id)

    if request.method == "POST":
        # Step 1: If the PIN check form was submitted
        if "verify_pin" in request.form:
            entered_pin = request.form["verify_pin"]
            if entered_pin == account.pin:
                # Correct PIN — allow editing
                return render_template("edit_account.html", account=account)
            else:
                flash("Incorrect PIN! Access denied.", "error")
                return redirect(url_for("view_accounts"))

        # Step 2: If the edit form was submitted
        account.fullname = request.form["fullname"]
        account.username = request.form["username"]
        account.email = request.form["email"]
        account.phone = request.form["phone"]
        account.dob = request.form["dob"]
        account.gender = request.form["gender"]
        account.address = request.form["address"]
        account.account_type = request.form["account_type"]
        account.branch = request.form["branch"]
        account.ifsc = request.form["ifsc"]
        account.pin = request.form["pin"]

        db.session.commit()
        flash("Account details updated successfully!", "success")
        return redirect(url_for("view_accounts"))

    # Step 3: Show PIN verification form first
    return render_template("verify_pin.html", account=account)


# ------------------------------
# DELETE ACCOUNT
# ------------------------------
@app.route("/delete_account/<int:id>", methods=["POST", "GET"])
def delete_account(id):
    account = Account.query.get_or_404(id)

    if request.method == "POST":
        pin = request.form.get("pin")

        if not pin:
            flash("Please enter your PIN to confirm deletion.", "error")
            return redirect(url_for("delete_account", id=id))

        if pin != account.pin:
            flash("Incorrect PIN! Account not deleted.", "error")
            return redirect(url_for("view_accounts"))

        db.session.delete(account)
        db.session.commit()
        flash("Account deleted successfully!", "success")
        return redirect(url_for("view_accounts"))

    # If method is GET — show confirmation page with PIN input
    return render_template("confirm_delete.html", account=account)


# ------------------------------
# REDIRECT HOME
# ------------------------------
@app.route("/home")
def home_redirect():
    return redirect(url_for("account_home"))

@app.route("/logout")
def logout():
    # Redirect to login page in auth-service
    return redirect("http://127.0.0.1:5000/login")  # or replace with your auth-service URL



# ------------------------------
# MAIN
# ------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

