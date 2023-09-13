# python3 -m uvicorn api:app --reload
#   Needs to provide:
    # 1.  Data points by day.
    # 2.  Moving average
    # 3.  Standard Deviation
    # 4.  Get days of consecutive data.
    # 5.  get data for last day.
    # 6.  Determine break outs
    # 7.  Determine blood in the streets & FOMO
    # 8. Low & high for 30 day, 7 day, 1 day, 1 hour, 1 minute.
    # 9. 10 second high low.
    # trigger last greatest pulse of fat finger.
    # 10. Gap up, gap down, percentage of gap.
    # 11. Acceleration / pulse, slow down, retreat, fail to continue.
    # 12. Average move in 1 minute,
    # 13. Average move in 10 seconds.
    # 14. Biggest move in 10 minutes.

# Step:
# 1.    Get given data points.


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


def select(sql):
    with psycopg.connect(f"dbname={dbname} user={dbuser}") as conn:
        # with conn.cursor(row_factory=class_row(Market)) as cur:
        # Connect to PostgreSQL from Python (Using SQL in Python) techTFQ
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

def get_last_id():
    sql = f'SELECT * FROM {dbtable} ORDER BY id DESC LIMIT 1'
    print(sql)
    stock = select(sql)
    print(stock)
    # print(stock[0])
    print('*****************************************************************')
    id = stock[0][0]
    print(id)
    return id

def get_stock(id):
    sql = f'SELECT * FROM {dbtable} WHERE id={id}'
    stock = select(sql)
    print(stock)
    return stock

def get_stocks():
    sql = f'SELECT * FROM {dbtable}'
    return select(sql)

def get_stocks_after(id):
    sql = f'SELECT * FROM {dbtable} WHERE id > {id}'
    return select(sql)


##############################################################################
#                                   API MODULE
@app.get("/", response_class=HTMLResponse)
def index() -> str:
    menu = """
    <html>
        <body>
            <title>Market API</title>
            <p>
            <h1>Market API End Points</h1>
            <a href="http://localhost:8000/lastid">Get last id</a><br>
            <a href="http://localhost:8000/after/28990">Get Market Data after id</a><br>
            <a href="http://localhost:8000/1/">Get Stock where id = 1</a><br>
            <a href="http://localhost:8000/all">Get all Market Data</a>
        </body>
    </html>
    """
    # return menu
    return HTMLResponse(content=menu, status_code=200)


@app.get("/all")
def get_all() -> dict:
    stocks = get_stocks()
    return {"market": stocks}


@app.get("/after/{id}")
def from_id(id) -> dict:
    stocks = get_stocks_after(id)
    return {'market': stocks}


@app.get("/lastid")
def lastid() -> dict:
    id = get_last_id()
    return {"last_id": id}

@app.get("/{id}")
def get_id(id) -> dict:
    stock = get_stock(id)
    return {'stock': stock}
