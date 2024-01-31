import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database.")
    except Exception as e:
        print(e)
    return conn


def create_table(conn):
    try:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT , shorturl text, longurl text NOT NULL)""")
        print("Table created.")
    except Exception as e:
        print(e)


def insert_urls(conn, shorturl, longurl):
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO urls (shorturl, longurl) VALUES (?, ?)""", (shorturl, longurl))
        conn.commit()
        print("Data inserted.")
    except Exception as e:
        print(e)


def fetch_longurl(conn, shorturl):
    try:
        c = conn.cursor()
        c.execute("""SELECT longurl FROM urls WHERE shorturl=?""", (shorturl,))
        return c.fetchone()[0]
    except Exception as e:
        return None


def fetch_all_shorturls(conn):
    try:
        c = conn.cursor()
        c.execute("""SELECT shorturl FROM urls""")
        res = c.fetchall()
        return [i[0] for i in res]
    except Exception as e:
        print(e)


def fetch_all_urls(conn):
    try:
        c = conn.cursor()
        c.execute("""SELECT * FROM urls""")
        res = c.fetchall()
        return res
    except Exception as e:
        print(e)


def delete_url(conn, id):
    try:
        c = conn.cursor()
        c.execute("""DELETE FROM urls WHERE id=?;""", (id,))
        res = c.fetchall()
        return res
    except Exception as e:
        print(e)