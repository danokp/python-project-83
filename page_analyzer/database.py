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

# db = Urls()
#
# print(db.get('name', 'https://google.com'))
# print(db.get_columns('id', ('id', 'name')))