# -*- coding: utf-8 -*-
"""
Server class contains all methods used to process request Get/Post that need manipulate with database
"""
from flask_web.create_data import insert_transaction #database module
from flask_web.portfolio_optimization import Generator #generate signal
import datetime
import requests

class WebServer():
    
    def __init__(self, mydatabase):
        self.mydatabase = mydatabase
        self.generator = Generator
        
    #---------------------------------------------
    def conn(self):
        '''
        create connect with database
        Returns
        -------
        return a connect obj
        '''
        #return self.mydatabase.connect() #for mysql
        return self.mydatabase #for postgresql
 
        
    #-------------------------------------------------------------------------    
    ''' INSERT REQUEST'''
    
    #---------------------------------------------
    def insert_transaction_request(self, form, user_id):
        """ insert a i4 of user's transactions to database
        Parameters
        ----------
        request : flask.request.form
            a form  contains terms : currency_index, status, price, day, volume 
        id : int, user's id number

        Returns
        -------
        None.
        """
        currency_index = form["currencyindex"]
        status = form["purchaseType"]
        price = form['price']
        day = form['datetime']
        volume = form['volume']
        
        #adjust format day
        time = datetime.datetime.strptime(day, "%Y-%m-%d")
        day = str(time.year) + "/" + str(time.month) + "/" + str(time.day)
        
        conn = self.conn()
        insert_transaction(conn, currency_index, status, price, day, volume, user_id)
        
        
    #-------------------------------------------------------------------------
    ''' GET REQUEST'''
    
    #--------------------------------------------
    def get_transaction_log(self, user_id, limit=0):
        conn = self.conn()
        cursor = conn.cursor()
        log_query = "select * from transactions where user_id= (%s) order by day desc"
        if limit > 0:
            log_query += " Limit " + str(limit)
        
        cursor.execute(log_query, (user_id,))
        data = cursor.fetchall()
        return data
        
    #--------------------------------------------
    def get_portfolio_by_user(self, user_id):
        conn = self.conn()
        cursor = conn.cursor()
        portfolio_query = "WITH define_qty AS (SELECT ROW_NUMBER() OVER (ORDER BY day) AS rank_day, \
                                    CASE \
                                    WHEN status = 'SELL' \
                                    THEN 0 - volume \
                                    ELSE volume \
                                    END AS qty, \
                            price, currency_index \
                            FROM transactions \
                            WHERE user_id = (%s) ) \
                            SELECT currency_index, SUM(qty) OVER (PARTITION BY currency_index ORDER BY rank_day) AS quant_cum, price \
                            FROM define_qty \
                            ORDER BY price "
        cursor.execute(portfolio_query, (user_id,))
        data = cursor.fetchall()
        return data
    
    
    #--------------------------------------------
    """ Get the current price of the currency pair
        Parameters
        ----------
         
        pair : string, currency pair's code

        Returns
        -------
        The pair's current price (float)
        """
    def get_current_pair_price(self, pair):
        API_URL = 'https://api.twelvedata.com/'
        API_KEY = 'ec344517980f4b9294a405e9ab48e346'
        params = {
        'symbol': pair,
        'apikey': API_KEY
        } 

        type_request = 'price'
        url = API_URL + type_request
        r = requests.get(url, params=params)

        if r.status_code != 200 and not 'values' in r.json().keys():
            print('Request error:', r.text)
            return None

        return float(r.json()['price'])
    
    
    #--------------------------------------------
    """ Get the price list from the current portfolio occupied by user
        Parameters
        ----------
         
        user_id : int, user's id number

        Returns
        -------
        The expected profit from the current portfolio occupied by user
        """
    def get_current_price_list(self, user_id):
        portfolio_data = self.get_portfolio_by_user(user_id)
        pair_list = []
        for i in range (len(portfolio_data)):
            pair_list.append(portfolio_data[i][0])
        
        cur_price_list = []
        for pair in pair_list:
            cur_price_list.append(self.get_current_pair_price(pair))
            
        return cur_price_list
    
    #--------------------------------------------
    """ Get the expected profit from the current portfolio occupied by user
        Parameters
        ----------
         
        user_id : int, user's id number

        Returns
        -------
        The expected profit from the current portfolio occupied by user
        """
        
    def get_expected_profit(self, cur_price_list, user_id):
        
        portfolio_data = self.get_portfolio_by_user(user_id)
        
        quant_cum_list = []
        price_list = []
        for i in range (len(portfolio_data)):
            quant_cum_list.append(portfolio_data[i][1])
            price_list.append(portfolio_data[i][2])
        
        profit_list = []
        
        for i in range(len(price_list)):
            profit_list.append(round((cur_price_list[i] - float(price_list[i])) * float(quant_cum_list[i]), 4))
        
        return profit_list
    
    #--------------------------------------------
    def get_crawl_data(self, limit=5):
        """Get a number of record from the data crawled in database 
        
        Parameters
        ----------
        limit : INT, optional equal 5
            The number of record 

        Returns
        -------
        data : list
        The data crawled

        """
        conn = self.conn()
        cursor = conn.cursor()
        query = "SELECT * FROM trading_data LIMIT " + str(limit)
      
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    
    #-----------------------------------------------
    def get_data_opt_port_chart(self, pair, indicators):
        '''Process request 201. The user sent currency index and list of indicators to plot chart. 
        This function will call optimize_portfolio module and return price data and buy/sell signal sequences
        

        Parameters
        ----------
        pair : Str, currency index.
        indicator : list[str], the name of indicators.

        Returns
        -------
        price : dict, close price
        signal : dict, buy/sell signal
        profit : )
        '''
        self.generator.set_database_conn(self.conn())
        result = self.generator.optimize_portfolio(cur=pair, indicator_list=indicators)
        price = result[0].to_json()
        signal = result[1].to_json()
        profit = str(round(result[2], 5))
        return price, signal, profit
        