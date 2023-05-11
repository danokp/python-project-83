import os
import psycopg2


DATABASE_URL = os.getenv('DATABASE_URL')


def initiate_conn():
    conn = psycopg2.connect(DATABASE_URL)
    return conn, conn.cursor()


def close_conn(conn, cur):
    cur.close()
    conn.close()


def insert_in_urls(conn, cur, url, date):
    cur.execute(
        f"INSERT INTO urls (name, created_at) VALUES ('{url}', '{date}');"
    )
    conn.commit()


def get_from_urls(cur, key, value):
    cur.execute(
        f"SELECT * FROM urls WHERE {key}='{value}';"
    )
    return cur.fetchone()


def get_columns_from_urls(cur, order_by, *args):
    cur.execute(
        f"SELECT {', '.join(*args)} FROM urls ORDER BY {order_by} DESC;"
    )
    return cur.fetchall()


def insert_in_urlchecks(
        conn,
        cur,
        status_code,
        h1, title,
        description,
        url_id,
        date,
):
    cur.execute(
        """INSERT INTO url_checks
        (url_id, status_code, h1, title, description, created_at)
        VALUES (%s, %s, %s, %s, %s, %s);
        """,
        (
            url_id,
            status_code,
            h1,
            title,
            description,
            date,
        )
    )
    conn.commit()


def get_columns_of_exact_url_from_urlchecks(cur, url_id, order_by, *args):
    cur.execute(
        f"""SELECT {', '.join(*args)} FROM url_checks
        WHERE url_id={url_id}
        ORDER BY {order_by} DESC;
        """
    )
    return cur.fetchall()


def get_last_check_info(cur):
    return cur.execute(
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


def join_urlchecks_with_urls(cur):
    cur.execute(
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
    return cur.fetchall()
