# Note: the module name is psycopg, not psycopg3
import psycopg

# Connect to an existing database
with psycopg.connect("dbname=samsuper user=samsuper") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stock1 (
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

        cur.execute("SELECT * FROM stock1")
        t = cur.fetchall()

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        print(t)
        for r in t:
            print(r[0], r[1], r[2])

        # Make the changes to the database persistent
        conn.commit()