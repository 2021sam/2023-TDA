# https://developer.tdameritrade.com/content/streaming-data#_Toc504640598
# print('If code executes then stops then you have an error in the code.')
# print('You will not get an error code.')
import pyodbc
import websockets
import asyncio
import datetime
import math
import json

# import Class.Stream
from Class.Stream import Stream
stream = Stream()

class StreamingClient():
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def DBconnect(self):
        server = 'DESKTOP-LBDSMI2'
        database = 'TDA'
        sql_driver = '{ODBC Driver 17 for SQL Server}'
        
        self.conn = pyodbc.connect( driver = sql_driver,
                                  server = server,
                                  database = database,
                                  trusted_connection = 'yes')
        self.cursor = self.conn.cursor()


    def insert( self, query, data_tuple):
        self.DBconnect()
        self.cursor.execute(query, data_tuple)
        self.conn.commit()
        self.conn.close()
        print(' ', end = '')
        

    def get_seconds( self, epoch):
        #epoch =  1593511118719 / 1000
        hours            = epoch % 86400            # Modding by seconds in a day  → Seconds since midnight 
        minutes          = hours % (60 * 60)        # Modding by seconds in a hour → Seconds since last hour
        seconds          = minutes % 60             # Modding by seconds in a minute → Seconds since last minute 
        #hour             = int( hours / 3600 )
        #minute           = int( minutes / 60 )
        #print ( '{}:{}:{}'.format( hour, minute, seconds ) )
        return seconds

    async def socketconnect(self):
        uri = 'wss://' + stream.userPrincipalsResponse['streamerInfo']['streamerSocketUrl'] + '/ws'
        self.connection = await websockets.client.connect(uri)
        if self.connection.open:
            print('Connection established.  Client correctly connected.')
            return self.connection

    async def send(self, message):
        await self.connection.send(message)


    async def receive(self, connection):
        previous_price = 0
        previous_epoch = 0

        while True:
            try:
                
                message = await connection.recv()
                message_decoded = json.loads(message)
                if 'data' in message_decoded.keys():
                    data = message_decoded['data'][0]
                    if 'content' in data.keys():
                        content = data['content']
                        for i in range( len(content) ):
                            k = ['3', '10']
                            if all(k in content[i] for k in ('3', '10')):
                                timestamp           = data['timestamp']
                                Symbol              = content[i]['key']
                                BidPrice            = 0.0
                                AskPrice            = 0.0
                                LastPrice           = 0.0
                                BidSize             = 0
                                AskSize             = 0
                                AskID               = ''
                                BidID               = ''
                                TotalVolume         = 0
                                LastSize            = 0
                                QuoteTime           = 0
                                HighPrice           = 0.0 #content['12']
                                LowPrice            = 0.0 #content['13']
                                BidTick             = '' #content['14'] #  Need to add
                                ClosePrice          = 0 #content['15']
                                ExchangeID          = '' #content['16']

                                if '1' in content[i].keys():
                                    BidPrice        = content[i]['1']

                                if '2' in content[i].keys():
                                    AskPrice        = content[i]['2']
                            
                                LastPrice           = content[i]['3']
                                
                                if '4' in content[i].keys():
                                    BidSize         = content[i]['4']
                                
                                if '5' in content[i].keys():
                                    AskSize         = content[i]['5']
                        
                                if '6' in content[i].keys():
                                    AskID           = content[i]['6']
                                
                                if '7' in content[i].keys():
                                    BidID           = content[i]['7']

                                if '8' in content[i].keys():
                                    TotalVolume     = content[i]['8']

                                if '9' in content[i].keys():
                                    LastSize        = content[i]['9']

                                TradeTime           = content[i]['10']

                                if '11' in content[i].keys():
                                    QuoteTime       = content[i]['11']

                                if '12' in content[i].keys():
                                    HighPrice       = content[i]['12']

                                if '13' in content[i].keys():
                                    LowPrice        = content[i]['13']
                                
                                if '14' in content[i].keys():
                                    BidTick         = content[i]['14']

                                if '15' in content[i].keys():
                                    ClosePrice      = content[i]['15']

                                if '16' in content[i].keys():
                                    ExchangeID      = content[i]['16']
                                    print('_16_', end = '')
                                   
                                query = 'INSERT INTO datastream (timestamp, Symbol, BidPrice, AskPrice, LastPrice, BidSize, AskSize, AskID, BidID, TotalVolume, LastSize, TradeTime, QuoteTime, HighPrice, LowPrice, BidTick, ClosePrice, ExchangeID) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                data_tuple = ( timestamp, Symbol, BidPrice, AskPrice, LastPrice, BidSize, AskSize, AskID, BidID, TotalVolume, LastSize, TradeTime, QuoteTime, HighPrice, LowPrice, BidTick, ClosePrice, ExchangeID )
                                self.insert(query, data_tuple)

                print('.', end = '')
                
            except websockets.exceptions.ConnectionClosed:
                print('Websocket connection is closed.')
                break


    async def heartbeat(self, connection):
        
        while True:
            try:
                await connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                print('Websocket connection is closed.')
                break