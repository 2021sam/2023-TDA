#   Checks for big moves in archived data

#   What I need
#   Search archive & get average & min & max moves
#   Use average & max moves to set breakpoint for live data.

import requests
import json

id1 = 1
id2 = 20
r = id2 - id1
stock = 'AAPL'
endpoint = f'http://localhost:8000/{stock}/{id1}/{id2}'
response_API = requests.get(endpoint)
data = response_API.text
data = json.loads(data)
data = data['stock']
# print(data["stock"])
# for e in data:
#     print(e)


def historic_trigger(data, breakpoint=1.5, moving_average_length=3):
    moving_average = []
    n = len(data)
    # print(f'n = {n}')
    moving_average_length = 3
    for i in range(n-1):
        # print(f'i = {i}')
        # print(data[i])
        # move = abs( close[i+1] - close[i] )
        move = abs( data[i+1][4] - data[i][4] )
        # print(f'move = {move}')
        moving_average.append(move)
        # print(moving_average)
        if len(moving_average) > moving_average_length:
            moving_average.pop(0)
            average = sum(moving_average) / moving_average_length
            print(f'average = {average}')
            if move > breakpoint * average:
                print(f'We got a BIG MOVE {move}!')


historic_trigger(data)