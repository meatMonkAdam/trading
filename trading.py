from zipline.api import*
from zipline import run_algorithm
from datetime import datetime
import pytz
import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt

# Setup our variables

def backtest(start, end, capital_base, func_name):
    def initialize(context):
        #creat a list to store one or multiple stocks' name
        context.stocks = symbols('AAPL')     
    
    def handle_data(context, data):
       
        # Load historical data for the stocks
        prices = data.history(context.stocks, 'price', 40, '1d')
        high = data.history(context.stocks, 'high', 40, '1d')
        low = data.history(context.stocks, 'low', 40, '1d')
        close = data.history(context.stocks, 'close', 40, '1d')
        signals = {}
        # Iterate over the list of stocks
        for stock in context.stocks:
            datas={'prices':prices[stock],'high':high[stock],'low':low[stock],'close':close[stock]
                    }
            signal = getattr(algo(), func_name)(datas)  

            signals[stock] = signal
            
            current_position = context.portfolio.positions[stock].amount
            #if signal less than 0 and we own same shares, we will sale some
            if signal < 0 and current_position > 0 and data.can_trade(stock):
                order_target(stock, 0)
            #if signal greater than 0 and we have 0 shares, we will buy some
            elif signal > 0 and current_position == 0 and data.can_trade(stock):
                order_target(stock, 100)
            #record signals of each stock   
            record(Signal=signals[stock],
                   price = data.current(stock, 'price'))   
            
            
    start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
    capital_base = 10000
    return run_algorithm(start, end, initialize,capital_base,handle_data,bundle = 'quandl')

class algo():
    def MACD(self,arg):
    #def MACD(self,price_stock,fastperiod, slowperiod, signalperiod):
        macd_raw, signal, hist = talib.MACD(np.array(arg['prices']))
        return hist[-1]
    
    def ADX(self,arg):
        signal = talib.ADX(np.array(arg['high']), np.array(arg['low']), np.array(arg['close']))
        return signal[-1]
    
    def ADXR(self,arg):
        signal = talib.ADXR(np.array(arg['high']), np.array(arg['low']), np.array(arg['close']),timeperiod = 13)
        return signal[-1]
    '''
    def xxx(self,arg):
        signal = talib.xxx(arg)
        return siganl
    '''
    


def make_graph(perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    perf.price.plot(ax=ax1)
    buys = perf.ix[[t > 0 for t in perf.Signal]]
    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    buys = perf_trans.ix[
        [t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax1.plot(buys.index, perf.price.ix[buys.index],
             '^', markersize=10, color='m')
    ax1.plot(sells.index, perf.price.ix[sells.index],
             'v', markersize=10, color='k')

    ax1.set_ylabel('price in $')
    ax2 = fig.add_subplot(2,1,2)
    perf.portfolio_value.plot(ax=ax2)

    ax1.set_ylabel('portfolio value in $')
    plt.show()
    
    
def analysis(perf):
    #value = perf.pnl
    fig = plt.figure()
    perf.returns.plot()
    plt.show()

    

    
perf = backtest(start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc),
             end = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc),
             capital_base = 100000000000,
             func_name = 'MACD')

make_graph(perf)
    
analysis(perf)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
