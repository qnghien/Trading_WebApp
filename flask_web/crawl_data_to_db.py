# !pip install websocket-client
# !pip install twelvedata[pandas]
# !pip install psycopg2

#libs needed
from twelvedata import TDClient
import time
import psycopg2 
import pandas as pd

conn = psycopg2.connect(
                  host="",
                  database="",
                  user="",
                  password="",
                  port= )

def crawl_data_to_db(conn,pair, interval, outputsize=5000, order="asc"):
    '''
    Function to crawl data from TwelveData trading platform using its API key
    based on users' request based on pair, interval, start date, end date (optional)

    default obervations are 5000 for 1 request
    8 requests per minutes - timesleep() is needed 
    '''
    API_URL = 'https://api.twelvedata.com/'
    API_KEY = '2fee87864f4b4e028b923774b84fb73c'

    # Initialize client - apikey parameter is required
    td = TDClient(apikey=API_KEY)
    cur = conn.cursor()

    ts = td.time_series(
        symbol=pair,
        interval=interval,
#         start_date=start_date,
#         end_date=end_date,
        outputsize=outputsize,
        order=order
    )
    
    result = ts.with_cci().with_macd().with_ema().with_rsi().with_stochrsi().with_supertrend().as_pandas()                                                
    time.sleep(60)
    result1 = ts.with_sma().with_wma().with_vwap().as_pandas()
    time.sleep(60)
    result_df = pd.merge(result,result1,on=['datetime','open', 'high', 'low', 'close'])
    result_df = result_df.reset_index()
    
    col = ['open', 'high', 'low', 'close', 
           'cci', 'macd', 'macd_signal', 'macd_hist', 'ema', 'rsi', 
            'fast_k', 'fast_d', 'supertrend', 'sma','wma','vwap']
    result_df[col] = result_df[col].round(5)

    query = "INSERT INTO trading_data (currency_index, date, open_price, high_price, low_price, close_price, cci, macd, macd_signal, macd_hist, ema, rsi, fast_k, fast_d, supertrend, sma, wma, vwap)"
    query += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for index, row in result_df.iterrows():
        try:
            cur.execute(query,(pair,row.datetime,row.open,row.high,row.low,\
                               row.close,row.cci,row.macd,row.macd_signal,row.macd_hist,row.ema,\
                               row.rsi,row.fast_k,row.fast_d,row.supertrend,row.sma,row.wma,row.vwap,))
        except Exception as e:
            print(e)    
        
    conn.commit()