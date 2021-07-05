from flask_web import app, session, webserver
from flask import render_template, redirect, url_for, request

#-----------------------------------------------------------------------------
def login_required(function):
    '''A Python Decorator
        It will ensure that the current user is logged in and authenticated 
    '''
    def login_wrapper(*args, **kwargs):
        if 'loggedin' in session and session['loggedin']:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    login_wrapper.__name__ = function.__name__
    return login_wrapper

#------------------------------------------------------------------------------
@app.route('/index', methods=["GET","POST"], endpoint="index")
@login_required
def index():
    log = webserver.get_transaction_log(session['id'], limit=8)
    pairs = sorted(set([ row[1] for row in log ]))
    stats = webserver.get_portfolio_by_user(session['id'])
    
    return render_template("index.html", len_list= len(pairs), 
                            list_currency=pairs, user_name=session['username'], log=log, stats=stats)
     

#------------------------------------------------------------------------------
@app.route('/optimize-portfolio', endpoint="optimize_portfolio")
@login_required
def optimize_portfolio():
    return render_template("optimize-portfolio.html", user_name=session['username'])

#------------------------------------------------------------------------------
@app.route('/data', endpoint="data_report")
@login_required
def data_report():
    log = webserver.get_transaction_log(session['id'])
    
    return render_template("data.html", user_name=session['username'], log=log)
    

#------------------------------------------------------------------------------
@app.route("/r", methods=["POST", "GET"], endpoint="process_request")
def process_request():
    '''Recive all request from client then classify them and sent to corresponding methods in server file
         categorical:
             1xx. INSERT  
                 + 100 : transaction into database
             
             -----------------------------------
             2xx. GET
                 + 200 : get
                 
            ------------------------------------
        NOTE: all request sent to /oder must spesify "type_request" term in form
        Examp: <input type="hidden" name="typeRequest" value="1"/>
    '''
    
    user_id = session['id']
    if request.method == "POST" and 'typeRequest' in request.form :
        if int(request.form['typeRequest']) == 100:
            webserver.insert_transaction_request(request.form, user_id)
        

    return redirect(url_for("index"))