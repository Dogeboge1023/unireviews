import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT symbol,shares FROM portfolio WHERE user_id = ? AND shares > 0", session["user_id"])
    check = db.execute("SELECT * FROM portfolio WHERE user_id=?", session["user_id"])
    if not check:
        return render_template("index.html")
    total_stock_value = 0
    for row in rows:
        symbol = row['symbol']
        shares = row['shares']
        price_list = lookup(symbol)
        price = price_list['price']
        row['price'] = usd(price)
        total_stock = round(float(price) * float(shares), 2)
        row['total_stock'] = usd(total_stock)
        total_stock_value += total_stock

    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    cash_left = (cash[0]['cash'])
    cash_for_html = usd(cash_left)
    total_all = usd(cash_left + total_stock_value)
    return render_template("index.html", stocks=rows, cash_left=cash_left, total_all=total_all, cash_for_html=cash_for_html)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Input symbol", 400)
        quote = lookup(symbol)
        if quote is None:
            return apology("Such stock doesnt exist", 400)
        shares_amount = request.form.get("shares")
        try:
            shares_amount = int(shares_amount)
        except ValueError:
            return apology("Shares amount must be a number", 400)
        if shares_amount < 1:
            return apology("Invalid shares amount", 400)
        cash_amount = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash_amount_actual = cash_amount[0]['cash']
        total_cost = quote["price"] * int(shares_amount)
        if cash_amount_actual < total_cost:
            flash("Not enough funds")
            return redirect("/buy")
        else:
            leftover_money = cash_amount_actual - total_cost

            db.execute("UPDATE users SET cash = :leftover_money WHERE id = :id",
                       leftover_money=leftover_money, id=session["user_id"])
            if db.execute("SELECT symbol FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol):
                db.execute("UPDATE portfolio SET shares = shares + ? WHERE user_id = ? AND symbol = ?",
                           shares_amount, session["user_id"], symbol)
                db.execute("INSERT INTO transactions(user_id, symbol, shares, price) VALUES(?,?,?,?)",
                           session["user_id"], symbol, shares_amount, quote["price"])
                flash("Bought!")
                return redirect("/")
            else:
                db.execute("INSERT INTO transactions(user_id, symbol, shares, price) VALUES(?,?,?,?)",
                           session["user_id"], symbol, shares_amount, quote["price"])
                db.execute("INSERT INTO portfolio(user_id, symbol, shares) VALUES(?,?,?)",
                           session["user_id"], symbol, shares_amount)
                flash("Bought!")
                return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id=?", session["user_id"])
    if not rows:
        flash("No history buy something at first")
        return redirect("/buy")
    else:
        for row in rows:
            symbol = row['symbol']
            shares = row['shares']
            price = row['price']
            row['price'] = usd(price)
            transacted = row['transacted']
    return render_template("history.html", stocks=rows)


@app.route("/login", methods=["GET", "POST"])  # completed log in but not by me
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Input Symbol", 400)
        quote = lookup(symbol)
        if quote is None:
            return apology("Invalid Symbol", 400)
        else:
            quote["price"] = usd(quote["price"])
            return render_template("quoted.html", quote=quote)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])  # completed register
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(rows) > 0:
            return apology("Username is taken", 400)
        if not username:
            return apology("Must provide username", 400)
        password = request.form.get("password")
        if not password:
            return apology("Must provide password", 400)
        confirm_password = request.form.get("confirmation")
        if not confirm_password:
            return apology("Must confirm password", 400)
        if password != confirm_password:
            return apology("Passwords do not match", 400)
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hashed_password)
        new_user_id = db.execute("SELECT id FROM users WHERE username = :username", username=username)
        session["user_id"] = new_user_id[0]['id']

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    rows = db.execute("SELECT symbol,shares FROM portfolio WHERE user_id =?", session["user_id"])
    check = db.execute("SELECT * FROM portfolio WHERE user_id=?", session["user_id"])
    cash_result = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    if not check:
        return apology("You dont own any shares", 400)
    for row in rows:
        symbol = row['symbol']
        shares_amount_db = row['shares']
        cash = cash_result[0]['cash']

    if request.method == "POST":
        shares_amount_input = request.form.get("shares")
        if not shares_amount_input:
            return apology("Choose amount", 400)
        shares_amount_input = int(shares_amount_input)
        if shares_amount_input < 1:
            return apology("Invalid amount", 400)
        symbol_input = request.form.get("symbol")
        if not symbol_input:
            return apology("Choose symbol to sell", 400)
        if shares_amount_db < shares_amount_input:
            return apology("You dont have that many shares bud", 400)
        price_stock = lookup(symbol)['price']
        total_giveout = price_stock * shares_amount_input
        total_new = float(cash) + float(total_giveout)
        new_shares_amount = shares_amount_db - shares_amount_input
        db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND symbol = ?",
                   new_shares_amount, session["user_id"], symbol)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", total_new, session["user_id"])
        db.execute("INSERT INTO transactions(user_id, symbol, shares, price) VALUES(?,?,-?,?)",
                   session["user_id"], symbol, shares_amount_input, price_stock)
        flash("Sold!")
        return redirect("/")
    return render_template("sell.html", stocks=rows)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    current_balance = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]['cash']
    current_balance = round(current_balance, 2)
    if request.method == "POST":
        added_cash = request.form.get("deposit")
        if not added_cash:
            flash("Input amount of cash you would like to deposit")
            return redirect("/deposit")
        added_cash = int(added_cash)
        if added_cash < 1:
            flash("Input valid number")
            return redirect("/deposit")
        new_cash = added_cash + current_balance
        print(new_cash)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
        flash("Deposit completed")
        return redirect("/deposit")
    return render_template("deposit.html", current_balance=current_balance)
