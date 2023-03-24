import psycopg2
import os


DATABASE_URL = os.getenv('DATABASE_URL')


class DataBase():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()



class Urls(DataBase):
    def insert(self, url, date):
        self.query(
            f"INSERT INTO urls (name, created_at) VALUES ('{url}', '{date}');"
        )
        self.commit()

    def get(self, key, value):
        self.query(
            f"SELECT * FROM urls WHERE {key}='{value}';"
        )
        return self.cur.fetchone()

    def get_columns(self, order_by, *args):
        self.query(
            f"SELECT {', '.join(*args)} FROM urls ORDER BY {order_by} DESC;"
        )
        return self.cur.fetchall()


class Url_checks(DataBase):
    def insert(self, url_id, date):
        self.query(
            f"INSERT INTO url_checks"
            f"(url_id, created_at) " # (url_id, status_code, h1, title, description, created_at)
            f"VALUES ('{url_id}', '{date}');"
        )
        self.commit()

    def get_columns_of_exact_url(self, url_id, order_by, *args):
        self.query(
            f"SELECT {', '.join(*args)} FROM url_checks "
            f"WHERE url_id={url_id} "
            f"ORDER BY {order_by} DESC;"
        )
        return self.cur.fetchall()