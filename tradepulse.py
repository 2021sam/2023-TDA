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
        self.changes_absolute = []
        self.fatfinger = False
        self.dead_cat_bounce = False
        self.continuation = False

        self.direction = 0      #   1 -> up, -1 -> down
        self.continuation_time = 0
        self.continuation_time_max = 0
        self.continuation_distance = 0
        self.continuation_distance_max = 0
        self.long = False
        self.short = False

    def append(self, price):
        self.price.append(price)
        self.n = len(self.price)
        if self.n > 1:
            direction = self.price[-1] - self.price[-2]
            # change = abs( self.price[-1] - self.price[-2] )
            change = abs( direction )
            self.changes.append(direction)
            self.changes_absolute.append(change)
            self.mean = sum(self.changes_absolute) / (self.n - 1)

        if self.n > 2:
            if self.changes[-2] * self.changes[-1] < 0:
                self.continuation_time = 1
                self.continuation_distance = self.changes[-1]
            else:
                self.continuation_time += 1
                self.continuation_distance += self.changes[-1]

            if self.continuation_time > self.continuation_time_max:
                self.continuation_time_max = self.continuation_time
                print(f'self.time_max: {self.continuation_time_max}')

            if self.continuation_distance > self.continuation_distance_max:
                self.continuation_distance_max = self.continuation_distance
                print(f'self.distance_max: {self.continuation_distance_max}')

            if change > self.max:
                self.max = change
                self.long = direction > 0
                self.short = direction < 0
                print(f'self.max = {self.max}')



stats = Stats('AAPL')
live = False
start_id = 1
last_live_id = 0
start_time = time.time()
lapse_time_seconds = 60


print('MAX     TIME    DISTANCE')

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

    # if stats.n > 1:
    #     print( max(stats.changes) )
    #     print(f'max: {stats.max:.2f}, continuation (time, distance): {stats.continuation_time:.2f}, {stats.continuation_distance:.2f}')
