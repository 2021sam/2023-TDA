import psycopg2 as psycopg
from psycopg2 import OperationalError, errorcodes, errors
from psycopg2 import __version__ as psycopg2_version


class DBTOOLS():
    def __init__(self, default_dbname, default_dbuser, default_dbpassword, dbname, dbuser, dbhost, dbpassword, dbport):
        self.default_dbname = default_dbname
        self.default_dbuser = default_dbuser
        self.default_dbpassword = default_dbpassword
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbhost = dbhost
        self.dbpassword = dbpassword
        self.dbport = dbport

    def db_exists(self):
        try:
            conn = psycopg.connect(
                dbname=self.dbname,
                user=self.dbuser,
                host=self.dbhost,
                password=self.dbpassword,
                port=self.dbport
            )
            exists = True
            cursor = conn.cursor()
            cursor.execute("select version();")
            r = cursor.fetchone()
            print(f'r={r}')
            # close the cursor object to avoid memory leaks
            cursor.close()
            # close the connection object also
            conn.close()

        except psycopg.OperationalError as err:
            print(f'OperationalError={err}')
            exists = False

        finally:
            return exists


    def db_create(self):
        try:
            conn = psycopg.connect(
                dbname=self.default_dbname,
                user=self.default_dbuser,
                host=self.dbhost,
                password=self.default_dbpassword,
                port=self.dbport
            )
            exists = True
            cursor = conn.cursor()
            print('db_create')
            sql = f'CREATE DATABASE {self.dbname} OWNER {self.dbuser};'
            print(sql)
            conn.autocommit = True  # Circumvent transaction block error
            cursor.execute(sql)
            # conn.commit()           #   ERROR: CREATE DATABASE cannot run inside a transaction block
            cursor.close()
            conn.close()

        except psycopg.OperationalError as err:
            print(f'OperationalError={err}')
            exists = False

        except psycopg.Error as e:
            print(f'ERROR: {e}')
            exists = False

        finally:
            return exists


    def table_exists(self, tablename):
        r = False
        with psycopg.connect(f"dbname={self.dbname} user={self.dbuser}") as conn:
            with conn.cursor() as cur:
                sql = f"""
                    select exists (select * from information_schema.tables where table_name='{tablename}');
                """
                cur.execute(sql)
                r = cur.fetchone()[0]
        return r

    def table_create(self, tablename):
        with psycopg.connect(f"dbname={self.dbname} user={self.dbuser}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {tablename} (
                        id SERIAL PRIMARY KEY,
                        timestamp BIGINT,
                        symbol varchar(4),
                        bidprice float,
                        askPrice float,
                        lastprice float,
                        bidsize integer,
                        asksize integer,
                        askid varchar(10),
                        bidid varchar(10),
                        totalvolume integer,
                        lastsize integer,
                        tradetime BIGINT,
                        quotetime BIGINT,
                        highprice float,
                        lowprice float,
                        bidtick varchar(10),
                        closeprice float,
                        exchangeid varchar(10))
                    """)
                conn.commit()
