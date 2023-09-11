import psycopg2 as psycopg


class DBTOOLS():
    def __init__(self, dbname, dbuser):
        self.dbname = dbname
        self.dbuser = dbuser

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
