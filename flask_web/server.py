# -*- coding: utf-8 -*-
"""
Server class contains all methods used to process request Get/Post that need manipulate with database
"""
from flask_web.create_data import insert_transaction #database module
import datetime

class WebServer():
    
    def __init__(self, mysql):
        self.mysql = mysql
        
        
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
        time = datetime.datetime.strptime(day, "%Y-%m-%dT%H:%M")
        day = str(time.year) + "/" + str(time.month) + "/" + str(time.day)
        
        conn = self.mysql.connect()
        insert_transaction(conn, currency_index, status, price, day, volume, user_id)
        
        
        
        
    #-------------------------------------------------------------------------
    ''' GET REQUEST'''
    
    #--------------------------------------------
    def get_transaction_log(self, user_id, limit=0):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        log_query = "select * from transaction where user_id= (%s) order by day desc"
        if limit > 0:
            log_query += " Limit " + str(limit)
        
        cursor.execute(log_query, (user_id,))
        data = cursor.fetchall()
        return data
        
    #--------------------------------------------
    def get_portfolio_by_user(self, user_id):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        portfolio_query = "WITH define_qty AS (SELECT ROW_NUMBER() OVER (ORDER BY day) AS rank_day, \
                                    CASE \
                                    WHEN status = 'SELL' \
                                    THEN 0 - volume \
                                    ELSE volume \
                                    END AS qty, \
                            price, currency_index \
                            FROM transaction \
                            WHERE user_id = (%s) ) \
                            SELECT currency_index, SUM(qty) OVER (PARTITION BY currency_index ORDER BY rank_day) AS quant_cum, price \
                            FROM define_qty \
                            ORDER BY price "
        cursor.execute(portfolio_query, (user_id,))
        data = cursor.fetchall()
        return data
    #--------------------------------------------
        