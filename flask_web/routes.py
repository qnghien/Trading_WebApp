from flask_web import app
from flask import render_template, redirect, url_for, request

#--------- Render ----------------------
@app.route('/')
@app.route('/dashboard', methods=["GET","POST"])
def index():
    pairs = ["USD/GBP", "USD/EUR", "USD/CHF", "USD/GPG"]
    return render_template("index.html", len_list= len(pairs), list_currency=pairs)

#------------------------------------------------------------------------------
@app.route('/optimize-portfolio')
def optimize_portfolio():
    
    return render_template("optimize-portfolio.html")

#------------------------------------------------------------------------------
@app.route('/data')
def data_report():
    return render_template("data.html")

#------------------------------------------------------------------------------
@app.route("/order", methods=["POST"])
def transaction_request():
    x = [att for att in request.form]
    return redirect(url_for("index"))