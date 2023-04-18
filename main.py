from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    count: int


# Note: the module name is psycopg, not psycopg3
import psycopg

def get_stocks():
    with psycopg.connect("dbname=samsuper user=samsuper") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM stock1")
            t = cur.fetchall()

            # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
            # of several records, or even iterate on the cursor
            print(t)
            # for r in t:
            #     print(r[0], r[1], r[2])
            return t



@app.get("/")
def index() -> dict:
    stocks = get_stocks()
    return {stocks[0]}
