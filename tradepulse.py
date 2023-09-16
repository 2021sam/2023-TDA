#   LIVE
#   Checks for big moves in archived data

#   What I need
#   Search archive & get average & min & max moves
#   Use average & max moves to set breakpoint for live data.

import requests
import json
from api_db import DB_Connect

stock = 'AAPL'

DBC = DB_Connect()


class Stats:
    def __init__(self, symbol):
        self.mean = 0
        self.max = 0
        self.n = 0
        self.symbol = symbol
        self.price = []
        self.changes = []

    def append(self, price):
        self.price.append(price)
        self.n = len(self.price)
        if self.n > 1:
            change = abs( self.price[-1] - self.price[-2] )
            self.changes.append(change)
            self.mean = sum(self.changes) / self.n

            if change > self.max:
                self.max = change


stats = Stats('AAPL')

while True:
    id = DBC.get_last_id()
    print( {"last_id": id} )
    stock = DBC.get_stock(id)
    # print( stock )
    if stock != stock[2]:
        continue

    stats.append(stock[5])
