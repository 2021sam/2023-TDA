# import pandas as pd
# import yfinance as yf
# import numpy as np
# import matplotlib.pyplot as plt
# data = yf.download('aapl')
# print( data.info )
import yfinance as yf
# Reference:
# pip install yfinance
msft = yf.Ticker("MSFT")
# get all stock info
msft.info
# get historical market data
hist = msft.history(period="1mo")
# print(hist)
# show meta information about the history (requires history() to be called first)
# print(msft.history_metadata)
# print(hist['Close'].values[0])
# close = hist['Close'].values
close = [v for v in hist['Close'].values]
# print(close)
# print(len(close))

moving_average = []
n = len(close)
m = 3
for i in range(n-1):
    # print(v
    move = abs( close[i+1] - close[i] )
    # print(move)
    moving_average.append(move)
    # print(moving_average)
    if len(moving_average) > m:
        moving_average.pop(0)
        average = sum(moving_average) / m
        # print(average)
        if move > 1.5 * average:
            print('We got a BIG MOVE !')

