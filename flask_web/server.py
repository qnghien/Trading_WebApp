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
    def get_transaction_log(self, user_id):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from transaction where user_id= (%s)", (user_id,))
        datas = cursor.fetchall()
        return datas
        
        