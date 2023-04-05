# Plot Live Stock Market candlestick data from a database
# This python script loops:
#  connects to a database
#  reads last record
#  plots data price point & volume

# Candlesticks.ipynb
# 07/04/2020
# Author Sam Portillo

# References:
#   https://oauth.net/2/
#   https://developer.tdameritrade.com/

# https://stackoverflow.com/questions/55837924/how-to-clear-tkinter-canvas-on-button-press

import math, pyodbc
import pandas as pd

class ReadSQL():
    def __init__(self):
        self.conn = None
        self.cursor = None


    def database_connect(self):
        server1 = 'DESKTOP-LBDSMI2'
        database1 = 'TDA'
        sql_driver = '{ODBC Driver 17 for SQL Server}'
        self.conn = pyodbc.connect( driver              = sql_driver,
                                    server              = server1,
                                    database            = database1,
                                    trusted_connection  = 'yes')
        self.cursor = self.conn.cursor()


    # https://pynative.com/python-mysql-select-query-to-fetch-data/
    # https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15
    def database_read( self ):
        sql_query = pd.read_sql_query("SELECT * FROM TDA.dbo.datastream where Symbol = '%s'" % 'SPY', self.conn )
        return sql_query


    def database_live( self ):
        sql_query = pd.read_sql_query('SELECT TOP (1) [id] \
              ,[timestamp]   \
              ,[Symbol] \
              ,[BidPrice] \
              ,[AskPrice] \
              ,[LastPrice] \
              ,[BidSize] \
              ,[AskSize] \
              ,[AskID] \
              ,[BidID] \
              ,[TotalVolume] \
              ,[LastSize] \
              ,[TradeTime] \
              ,[QuoteTime] \
              ,[HighPrice] \
              ,[LowPrice] \
              ,[BidTick] \
              ,[ClosePrice] \
              ,[ExchangeID] \
          FROM [TDA].[dbo].[datastream] \
          ORDER BY id DESC', self.conn)
        return sql_query
