# riththy_app/utils/mysql_connection.py
import mysql.connector
from django.conf import settings


def get_mysql_connection():
    """
    Returns a raw mysql.connector connection.
    Best for your store_telegram_update() function.
    """
    db = settings.DATABASES['default']

    try:
        conn = mysql.connector.connect(
            host=db['HOST'],
            user=db['USER'],
            password=db['PASSWORD'],
            database=db['NAME'],
            port=int(db.get('PORT', 3306)),
            autocommit=True,          # Important for your store function
            charset='utf8mb4',        # Good for emojis and Khmer text
            collation='utf8mb4_unicode_ci',
        )
        conn.close()
        return True
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL Connection Error: {err}")
        raise


def fetch_data_from_table(table_name: str):
    """
    Fetch all rows from a table as list of dicts.
    """
    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()


# Optional: Simple Django ORM cursor wrapper (if you need it)
from django.db import connection as django_connection

def get_django_cursor():
    """Use only when you want to use Django's ORM connection"""
    return django_connection.cursor()