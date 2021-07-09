from flask_web import app, session, webserver
from flask import render_template, redirect, url_for, request, jsonify

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
    currency_list = webserver.generator.get_cur_list()
    indicators = list(webserver.generator.get_indicators().keys())
    
    return render_template("optimize-portfolio.html", user_name=session['username'],
                           currency_list=currency_list, indicators=indicators)

#------------------------------------------------------------------------------
@app.route('/data', endpoint="data_report")
@login_required
def data_report():
    log = webserver.get_transaction_log(session['id'])
    crawl_data = webserver.get_crawl_data()
    col_crawl_data = ['id', 'currency_index', 'date', 'open_price', 'high_price', 'low_price', 
                      'close_price', 'cci', 'macd', 'macd_signal', 'macd_hist', 'ema', 'rsi', 
                      'fast_k', 'fast_d', 'supertrend', 'sma', 'wma', 'vwap']
    return render_template("data.html", user_name=session['username'], log=log, crawl_data=crawl_data,
                           col_crawl_data = col_crawl_data)
    
#------------------------------------------------------------------------------
@app.route("/user-guide")
def user_guide():
    return render_template("user-guide.html")
 

#------------------------------------------------------------------------------
@app.route("/r", methods=["POST", "GET"], endpoint="process_request")
def process_request():
    '''Recive all request from client then classify them and sent to corresponding methods in server file
         categorical:
             1xx. POST 
                 + 100 : transaction into database (form format)
                 + 101 : sent stat-data(Json format) to get profit
             
             -----------------------------------
             2xx. GET
                 + 200 : get current price, include 2 args in request are 'typeRequest' and 'list_currency'
                 + 201 : get plot for portfolio optimization page
                 
            ------------------------------------
        NOTE: all request sent to process_request must spesify "type_request" term in form
        Examp: <input type="hidden" name="typeRequest" value="1xx"/> in form
            or data:{'typeRequest': "2xx"} in ajax function
    '''
    
    user_id = session['id']
    #post requests
    if request.method == "POST":
        #100
        if 'typeRequest' in request.form and int(request.form['typeRequest']) == 100:
            webserver.insert_transaction_request(request.form, user_id)
            return redirect(url_for("index"))
        
        
        #101
        if request.is_json:
            jsondata = request.get_json()
            if "typeRequest" in jsondata.keys() and int(jsondata['typeRequest']) == 101:
                cur_price_list = [float(value) for value in jsondata['data']]
                profit_list = webserver.get_expected_profit(cur_price_list=cur_price_list, user_id=session['id'])
                return jsonify({'profit_list': profit_list})
        
        

    #get requests
    if request.method == "GET":
        #200
        if "typeRequest" in request.args and int(request.args.get("typeRequest")) == 200:
            cur_price_list = webserver.get_current_price_list(user_id=session['id'])   
            return jsonify({'cur_price_list': cur_price_list})
    
        #201
        if "typeRequest" in request.args and int(request.args.get("typeRequest")) == 201:
            pair = request.args["pair"].replace("-", "/")
            indicators = request.args["indicators"].split("+")
            price, signal, exp_profit = webserver.get_data_opt_port_chart(pair=pair, indicators=indicators)
            return jsonify({"exp_profit":exp_profit, 'price':price, "signal":signal})
    
    #other
    return redirect(url_for("index"))