import os
import psycopg2


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


class UrlChecks(DataBase):
    def insert(self, status_code, h1, title, description, url_id, date):
        self.query(
            f"""INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (
                {url_id},
                {status_code},
                '{h1}',
                '{title}',
                '{description}',
                '{date}'
            );
            """
        )
        self.commit()

    def get_columns_of_exact_url(self, url_id, order_by, *args):
        self.query(
            f"""SELECT {', '.join(*args)} FROM url_checks
            WHERE url_id={url_id}
            ORDER BY {order_by} DESC;
            """
        )
        return self.cur.fetchall()

    def get_last_check_info(self):
        return self.query(
            """SELECT
                url_checks.id,
                url_checks.url_id,
                url_checks.status_code,
                url_checks.created_at
            FROM url_checks
            JOIN
            (SELECT url_id, MAX(id) AS max_id FROM url_checks GROUP BY url_id)
            AS url_checks2
            ON url_checks.id = url_checks2.max_id
            ORDER BY url_checks.url_id DESC;
            """)

    def join_with_urls(self):
        self.query(
            """SELECT
                urls.id AS url_id,
                urls.name,
                url_checks.created_at,
                url_checks.status_code
            FROM urls
            LEFT JOIN (
                SELECT url_id, MAX(id) AS max_id
                FROM url_checks
                GROUP BY url_id
            ) AS latest_checks
            ON urls.id = latest_checks.url_id
            LEFT JOIN url_checks
            ON latest_checks.max_id = url_checks.id
            ORDER BY url_id DESC;
            """)
        return self.cur.fetchall()
