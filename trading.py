from zipline.api import*
from zipline import run_algorithm
from datetime import datetime
import pytz
import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt

# Setup our variables

def start(start, end, capital_base, algo):
    def initialize(context):
        #creat a list to store one or multiple stocks' name
        context.stocks = symbols('AAPL')     
    
    def handle_data(context, data):
       
        # Load historical data for the stocks
        prices = data.history(context.stocks, 'price', 40, '1d')
        signals = {}
        
        # Iterate over the list of stocks
        for stock in context.stocks:
            #choose which algo to use
            if algo=='MACD':
                signal = algo_MACD(prices[stock],fastperiod=12, slowperiod=26, signalperiod=9)
            #if algo=='some_name':
                #signal=algo_some_name()
                
            #store the signal for further inspect
            signals[stock] = signal
            
            current_position = context.portfolio.positions[stock].amount
            #if signal less than 0 and we own same shares, we will sale some
            if signal < 0 and current_position > 0 and data.can_trade(stock):
                order_target(stock, 0)
            #if signal greater than 0 and we have 0 shares, we will buy some
            elif signal > 0 and current_position == 0 and data.can_trade(stock):
                order_target(stock, 100)
            #record signals of each stock   
            record(Signal=signals[stock])   
            
            
    start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    capital_base = 10000
    return run_algorithm(start, end, initialize,capital_base,handle_data,bundle = 'quandl')


def algo_MACD(price_stock,fastperiod=12, slowperiod=26, signalperiod=9):
    macd_raw, signal, hist = talib.MACD(np.array(price_stock), fastperiod, slowperiod, signalperiod)
    return hist[-1]
    
    

    
perf = start(start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc),
             end = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc),
             capital_base = 10000,
             algo = 'MACD')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    