import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connect(self):
        return psycopg2.connect(self.db_url)

    def get_content_urls(self):
        with self.get_connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute(
                    '''
                    SELECT
                        urls.id as id,
                        urls.name as name,
                        url_checks.status_code as code,
                        url_checks.created_at as last_check
                    FROM urls
                    LEFT JOIN url_checks ON
                        url_checks.id = (
                            SELECT url_checks.id
                            FROM url_checks
                            WHERE urls.id = url_checks.url_id
                            ORDER BY url_checks.created_at ASC
                            LIMIT 1
                        )
                    ORDER BY urls.id DESC
                    '''
                )
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
        current_date = datetime.now().strftime('%Y-%m-%d')
        with self.get_connect() as conn:
            with conn.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id
                    ''',
                    (url_data['url'], current_date)
                )
                return c.fetchone()[0]

    def get_checks(self, id):
        with self.get_connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute('''
                          SELECT * FROM url_checks
                          WHERE url_id = %s
                          ORDER BY id DESC''', (id,))
                return c.fetchall()

    def save_check_url(self, id):
        current_date = datetime.now().strftime('%Y-%m-%d')
        with self.get_connect() as conn:
            with conn.cursor() as c:
                c.execute(
                    '''
                    INSERT INTO url_checks (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description,
                        created_at
                        )
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    ''',
                    (id, 0, '', '', '', current_date)
                )
                return c.fetchone()[0]
