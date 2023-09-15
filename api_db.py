import psycopg2 as psycopg
# import psycopg2
# from psycopg.rows import class_row
import psycopg2.extras

from dataclasses import dataclass
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from private.credentials import default_dbname, default_dbuser, default_dbpassword, dbname, dbuser, dbhost, dbpassword, dbport, dbtable
app = FastAPI()


@dataclass
class Market:
    id: int
    timestamp: int
    symbol: str
    bidprice: float
    askprice: float
    lastprice: float
    bidsize: int
    asksize: int
    askid: str
    bidid: str
    totalvolume: int
    lastsize: int
    tradetime: int
    quotetime: int
    highprice: float
    lowprice: float
    bidtick: str
    closeprice: float
    exchangeid: str

class DB_Connect:
    def __init__(self):
        pass

    def select(self, sql):
        with psycopg.connect(f"dbname={dbname} user={dbuser}") as conn:
            # with conn.cursor(row_factory=class_row(Market)) as cur:
            # Connect to PostgreSQL from Python (Using SQL in Python) techTFQ
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def get_last_id(self):
        sql = f'SELECT * FROM {dbtable} ORDER BY id DESC LIMIT 1'
        # print(sql)
        stock = self.select(sql)
        # print(stock)
        # print(stock[0])
        # print('*****************************************************************')
        id = stock[0][0]
        # print(id)
        return id

    def get_stock(self, id):
        sql = f'SELECT * FROM {dbtable} WHERE id={id}'
        stock = self.select(sql)
        # print(stock)
        return stock

    def get_stocks(self):
        sql = f'SELECT * FROM {dbtable}'
        return self.select(sql)

    def get_stocks_after(self, id):
        sql = f'SELECT * FROM {dbtable} WHERE id > {id}'
        return self.select(sql)

    def get_stocks_from_to(self, symbol, id1, id2):
        sql = f'''SELECT * FROM {dbtable} WHERE id >= {id1} AND id <= {id2} AND symbol = '{symbol}';'''
        print(sql)
        return self.select(sql)
