# # inventory/utils/db_connection.py
# import hashlib
# from django.db import connections
# from contextlib import contextmanager
# import pymysql
# inventory/utils/db_connection.py
import hashlib
from django.db import connections
import pymysql
from contextlib import contextmanager
from django.conf import settings

# inventory/utils/db_connection.py
import hashlib
from django.db import connections
import pymysql
from contextlib import contextmanager

def get_dynamic_db_alias(db_name: str) -> str:
    """Generate unique alias for dynamic database"""
    return f"dynamic_{hashlib.md5(db_name.encode()).hexdigest()[:12]}"


def register_dynamic_database(db_name: str):
    """Register a new database name using default credentials"""
    alias = get_dynamic_db_alias(db_name)

    if alias not in connections.databases:
        default_db = connections.databases['default']
        connections.databases[alias] = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_name,
            'USER': default_db['USER'],
            'PASSWORD': default_db['PASSWORD'],
            'HOST': default_db.get('HOST', 'localhost'),
            'PORT': default_db.get('PORT', '3306'),
            'OPTIONS': {'charset': 'utf8mb4'},
            'CONN_MAX_AGE': 0,
        }

    return alias


@contextmanager
def mysql_connection():
    db = settings.DATABASES["default"]

    conn = pymysql.connect(
        host=db["HOST"],
        user=db["USER"],
        password=db["PASSWORD"],
        database=db["NAME"],
        port=int(db.get("PORT", 3306)),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        ssl=db.get("OPTIONS", {}).get("ssl", None),
        connect_timeout=5
    )

    try:
        yield conn
    finally:
        conn.close()
# def get_dynamic_db_alias(db_name: str) -> str:
#     """Generate safe alias from database name"""
#     return f"dynamic_{hashlib.md5(db_name.encode()).hexdigest()[:12]}"


# def register_dynamic_database(db_name: str, 
#                               host='localhost', 
#                               user=None, 
#                               password=None, 
#                               port=3306, 
#                               charset='utf8mb4'):
#     """
#     Register a new database (different NAME) on the same MySQL server.
#     Uses the same credentials as 'default' unless overridden.
#     """
#     if not user or not password:
#         # Fallback to default credentials from settings
#         default_db = connections.databases['default']
#         user = default_db['USER']
#         password = default_db['PASSWORD']
#         host = default_db.get('HOST', host)
#         port = default_db.get('PORT', port)

#     alias = get_dynamic_db_alias(db_name)

#     if alias not in connections.databases:
#         connections.databases[alias] = {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': db_name,                    # <-- This is the only thing that changes
#             'USER': user,
#             'PASSWORD': password,
#             'HOST': host,
#             'PORT': str(port),
#             'OPTIONS': {'charset': charset},
#             'CONN_MAX_AGE': 0,                  # Close after request for dynamic safety
#         }

#     return alias


# @contextmanager
# def mysql_connection(db_name: str, host='localhost', user=None, password=None, port=3306):
#     """Manual raw pymysql connection (when you need full control)"""
#     conn = None
#     try:
#         if not user or not password:
#             default = connections.databases['default']
#             user = default['USER']
#             password = default['PASSWORD']
#             host = default.get('HOST', host)

#         conn = pymysql.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name,
#             port=port,
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         yield conn
#     finally:
#         if conn:
#             conn.close()