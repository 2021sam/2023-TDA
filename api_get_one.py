import requests
import json

# response_API = requests.get('http://localhost:8000/1')
# print(response_API.status_code)

# data = response_API.text
# data = json.loads(data)
# print(data["stock"])

stock = []
for i in range(1, 100):
    endpoint = f'http://localhost:8000/{i}'
    print(endpoint)
    r = requests.get(endpoint)
    d = json.loads( r.text )
    for e in d['stock']:
        print(e[0], e[2], e[3])
        stock.append(e[0])

# moving_average = []
# n = len(close)
# m = 3
# for i in range(n-1):
#     # print(v
#     move = abs( close[i+1] - close[i] )
#     # print(move)
#     moving_average.append(move)
#     # print(moving_average)
#     if len(moving_average) > m:
#         moving_average.pop(0)
#         average = sum(moving_average) / m
#         # print(average)
#         if move > 1.5 * average:
#             print('We got a BIG MOVE !')


