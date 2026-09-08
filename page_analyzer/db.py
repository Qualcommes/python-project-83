import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv()


def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    return psycopg.connect(database_url, row_factory=dict_row)


def get_all_urls():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Получаем все URL и дату последней проверки для каждого из них
            cursor.execute(
                """
                SELECT 
                    urls.id, 
                    urls.name, 
                    MAX(url_checks.created_at) AS last_check
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id, urls.name
                ORDER BY urls.id DESC;
                """
            )
            return cursor.fetchall()


def find_url_by_name(name):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, created_at FROM urls WHERE name = %s",
                (name,)
            )
            return cursor.fetchone()


def find_url_by_id(url_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, created_at FROM urls WHERE id = %s",
                (url_id,)
            )
            return cursor.fetchone()


def add_url(name):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO urls (name)
                VALUES (%s)
                RETURNING id;
                """,
                (name,)
            )
            result = cursor.fetchone()
            conn.commit()
            return result['id']


def add_url_check(url_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks (url_id)
                VALUES (%s)
                RETURNING id;
                """,
                (url_id,)
            )
            result = cursor.fetchone()
            conn.commit()
            return result['id']


def get_url_checks(url_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC;
                """,
                (url_id,)
            )
            return cursor.fetchall()