#   LIVE
#   Checks for big moves in archived data

#   What I need
#   Search archive & get average & min & max moves
#   Use average & max moves to set breakpoint for live data.

import requests
import json
from api_db import DB_Connect

id1 = 1
id2 = 100
r = id2 - id1
stock = 'AAPL'

DBC = DB_Connect()

id = DBC.get_last_id()
print( {"last_id": id} )

stock = DBC.get_stock(id)
print( stock )


# endpoint = f'http://localhost:8000/{stock}/{id1}/{id2}'
# response_API = requests.get(endpoint)
# data = response_API.text
# data = json.loads(data)
# data = data['stock']
# # print(data["stock"])
# # for e in data:
# #     print(e)


# def historic_mean_max(data):
#     changes = []
#     max = 0
#     n = len(data)
#     # print(f'n = {n}')

#     for i in range(n-1):
#         # print(f'i = {i}')
#         # print(data[i])
#         change = abs( data[i+1][4] - data[i][4] )
#         changes.append(change)

#         if change > max:
#             max = change

#     mean = sum(changes) / n
#     print(f'average = {mean}')

#     return mean, max


# max = historic_mean_max(data)
# print(max)
