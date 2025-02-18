import psycopg2
from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connect(self):
        return psycopg2.connect(self.db_url)

    def get_content_urls(self):
        with self.get_connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM urls ORDER BY id DESC")
                return c.fetchall()

    def find_urls_by_name(self, name):
        with self.get_connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM urls WHERE name=%s", (name,))
                return c.fetchone()

    def find_urls_by_id(self, id):
        with self.get_connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM urls WHERE id=%s", (id,))
                return c.fetchone()

    def save_urls(self, url_data):
        with self.get_connect() as conn:
            with conn.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO urls (name)
                    VALUES (%s) RETURNING id
                    ''',
                    (url_data['url'],)
                )
                return c.fetchone()[0]
