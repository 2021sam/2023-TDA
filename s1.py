#   2023.04.10 - Working

# pip install python-dateutil
import websocket        # pip install websocket-client
import json, urllib
from datetime import datetime
from Class.Stream import Stream
stream = Stream()
file_name = 'message4.json'
subscribed = 0
message_count = 0
m = 0
def on_message(ws, message):
    global subscribed
    global message_count
    message_json = json.loads(message)
    print("*****Received message")
    print(message)
    
    # d = {m: message }

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
