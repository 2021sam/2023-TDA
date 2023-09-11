import psycopg2 as psycopg
from private.credentials import default_dbname, default_dbuser, default_dbpassword, dbname, dbuser, dbhost, dbpassword, dbport
from db_tools import DBTOOLS


def init_db(db):
    exists = False
    while not exists:
        exists = db.db_exists()
        print(f'db exists = {exists}')
        if not exists:
            db.db_create()


def init_db_table(db):
    exists = False
    while not exists:
        exists = db.table_exists('stock')
        print(f'table exists = {exists}')
        if not exists:
            db.table_create('stock')

db = DBTOOLS(default_dbname, default_dbuser, default_dbpassword, dbname, dbuser, dbhost, dbpassword, dbport)
init_db(db)
init_db_table(db)
