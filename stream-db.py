#   2023.04.10 - Working

# pip install python-dateutil
import websocket        # pip install websocket-client
import json, urllib
import psycopg
from datetime import datetime
from TDA.Stream import Stream

stream = Stream()
file_name = 'stock1.json'
subscribed = 0
message_count = 0
m = 0
def on_message(ws, message):
    global subscribed
    global message_count
    message_json = json.loads(message)
    print("*****Received message")
    # print(message)
    if 'data' in message_json:
        data = message_json['data'][0]
        # print(data.keys())
        if 'content' in data.keys():
            content = data['content']
            extract_stock_content(data['timestamp'], content)
        # ['service', 'timestamp', 'command', 'content']
        # print( data['service'] )
        # print( data['timestamp'] )
        # print( data['command'] )
        # print( data['content'] )
        # print( data['content'])


    f = open(file_name, "a")
    f.write(message + ',\n')
    f.close()

    if subscribed == 0:
        subscribed = 1
        print("*****Subscribing to quote")
        print(stream.qos)
        ws.send(stream.qos)
        ws.send(stream.quote_sub)


    if subscribed == 1 and message_count == 0:
        message_count = 1
        print(stream.quote_sub)


    if message_count > 0:
        message_count += 1
    # else:
    #     print("***************")
    #     message_count += 1
    #     if message_count == 50:
    #         print("*****Unsubscribing to quote")
    #         print(stream.quote_unsub)
    #         ws.send(stream.quote_unsub)


def on_error(ws, error):
    print(error)

def on_open(ws):
    # Subscribe to real-time data
    print("Connection open. Send the auth message")
    print(stream.login)
    ws.send(stream.login)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed with status code:", close_status_code)
    print("Close message:", close_msg)


def extract_stock_content(timestamp, content):
    for i in range( len(content) ):
        k = ['3', '10']
        if all(k in content[i] for k in ('3', '10')):
            timestamp           = timestamp
            symbol              = content[i]['key']
            bidprice            = 0.0
            askprice            = 0.0
            lastprice           = 0.0
            bidsize             = 0
            asksize             = 0
            askid               = ''
            bidid               = ''
            totalvolume         = 0
            lastsize            = 0
            quotetime           = 0
            highprice           = 0.0 #content['12']
            lowprice            = 0.0 #content['13']
            bidtick             = ''  #content['14'] #  Need to add
            closeprice          = 0   #content['15']
            exchangeid          = ''  #content['16']

            if '1' in content[i].keys():
                bidprice        = content[i]['1']

            if '2' in content[i].keys():
                askprice        = content[i]['2']
            lastprice           = content[i]['3']
            
            if '4' in content[i].keys():
                bidsize         = content[i]['4']
            
            if '5' in content[i].keys():
                asksize         = content[i]['5']
    
            if '6' in content[i].keys():
                askid           = content[i]['6']
            
            if '7' in content[i].keys():
                bidid           = content[i]['7']

            if '8' in content[i].keys():
                totalvolume     = content[i]['8']

            if '9' in content[i].keys():
                lastsize        = content[i]['9']
            tradetime           = content[i]['10']

            if '11' in content[i].keys():
                quotetime       = content[i]['11']

            if '12' in content[i].keys():
                highprice       = content[i]['12']

            if '13' in content[i].keys():
                lowprice        = content[i]['13']
            
            if '14' in content[i].keys():
                bidtick         = content[i]['14']

            if '15' in content[i].keys():
                closePrice      = content[i]['15']

            if '16' in content[i].keys():
                exchangeid      = content[i]['16']
                print('_16_', end = '')

            data_tuple = ( timestamp, symbol, bidprice, askprice, lastprice, bidsize, asksize, askid, bidid, totalvolume, lastsize, tradetime, quotetime, highprice, lowprice, bidtick, closeprice, exchangeid )
            query = f'INSERT INTO stock1 (timestamp, symbol, bidprice, askprice, lastprice, bidsize, asksize, askid, bidid, totalvolume, lastsize, tradetime, quotetime, highprice, lowprice, bidtick, closeprice, exchangeid) VALUES {data_tuple}'
            print('query')
            print(query)
            print('.')
            insert(query, data_tuple)

def insert(query, data_tuple):
    with psycopg.connect("dbname=samsuper user=samsuper") as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()


f = open(file_name, "w+")
f.write('[\n')
f.close()
websocket.enableTrace(True)
websocket_url = 'wss://' + stream.principals['streamerInfo']['streamerSocketUrl'] + '/ws'
print(websocket_url)
ws = websocket.WebSocketApp(websocket_url,
                            on_message=on_message,
                            on_error=on_error,
                            on_open=on_open,
                            on_close=on_close)

ws.run_forever()
