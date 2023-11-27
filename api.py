import psycopg2 as psycopg
import psycopg2.extras

from dataclasses import dataclass
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from private.credentials import default_dbname, default_dbuser, default_dbpassword, dbname, dbuser, dbhost, dbpassword, dbport
from api_db import DB_Connect
app = FastAPI()
DBC = DB_Connect()
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
            <a href="/lastid">Get last id</a><br>
            <a href="/after/28990">Get Market Data after id</a><br>
            <a href="/1/">Get Stock where id = 1</a><br>
            <a href="/all">Get all Market Data</a>
        </body>
    </html>
    """
    # return menu
    return HTMLResponse(content=menu, status_code=200)

@app.get("/all")
def get_all() -> dict:
    stocks = DBC.get_stocks()
    return {"market": stocks}

@app.get("/after/{id}")
def from_id(id) -> dict:
    stocks = DBC.get_stocks_after(id)
    return {'market': stocks}

@app.get("/lastid")
def lastid() -> dict:
    id = DBC.get_last_id()
    return {"last_id": id}

@app.get("/{id}")
def get_id(id) -> dict:
    stock = DBC.get_stock(id)
    return {'stock': stock}

@app.get("/{symbol}/{id1}/{id2}")
def from_to_id(symbol, id1, id2) -> dict:
    print(symbol, id1, id2)
    stocks = DBC.get_stocks_from_to(symbol, id1, id2)
    return {'stock': stocks}
