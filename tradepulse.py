#   Checks for big moves in archived & live data

import requests
import json
import time
from api_db import DB_Connect

DBC = DB_Connect()
symbol = 'AAPL'

class Stats:
    def __init__(self, symbol):
        self.mean = 0
        self.max = 0
        self.n = 0
        self.symbol = symbol
        self.price = []
        self.changes = []
        self.fatfinger = False
        self.continuation = False
        self.long = False
        self.short = False

    def append(self, price):
        self.price.append(price)
        self.n = len(self.price)
        if self.n > 1:
            direction = self.price[-1] - self.price[-2]
            change = abs( self.price[-1] - self.price[-2] )
            self.changes.append(change)
            self.mean = sum(self.changes) / (self.n - 1)

            if change > self.max:
                self.max = change
                self.long = direction > 0
                self.short = direction < 0



stats = Stats('AAPL')
live = False
start_id = 1
last_live_id = 0
start_time = time.time()
lapse_time_seconds = 10


while start_time + lapse_time_seconds > time.time():
    time.sleep(1)
    if live:
        id = DBC.get_last_id()
        if last_live_id == id:
            continue

        last_live_id = id

    else:
        id = start_id
        start_id += 1
    # print( {"id": id} )
    stock = DBC.get_stock(id)
    # print( stock )
    stock = stock[0]
    # print(stock)
    if symbol != stock[2]:
        continue

    stats.append(stock[5])
    # print(stats.price)
    # print(stats.mean, max(stats.changes))
    if stats.n > 1:
        print( max(stats.changes) )
