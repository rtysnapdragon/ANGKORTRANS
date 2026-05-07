from django.db import connections
from django.db.utils import OperationalError
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS, connection

def get_dynamic_connection(db_name: str) -> str:
    if db_name not in connections.databases:
        # Clone the default DB settings but change NAME
        connections.databases[db_name] = {
            **settings.DATABASES['default'],
            'NAME': db_name,
        }
    return db_name

def validate_database_and_table22(db_name: str, model_class):
    """
    Validates that:
    1. The database exists.
    2. The main table for the model exists.
    3. All related tables (ForeignKey/OneToOne) exist.

    Args:
        db_name: The target database name
        model_class: Django model class to validate

    Returns:
        - (True, None) if all checks pass
        - (False, Response) if any check fails
    """
    if not db_name:
        return False, Response(
            {'error': 'Missing Rty-Database header'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with connections['default'].cursor() as cursor:
            # 1. Check if database exists
            cursor.execute("SHOW DATABASES")
            all_dbs = [row[0] for row in cursor.fetchall()]

        if db_name not in all_dbs:
            return False, Response(
                {'error': f'Database "{db_name}" not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Helper to check table existence
        def table_exists(table_name):
            with connections['default'].cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = %s AND table_name = %s
                """, [db_name, table_name])
                (exists,) = cursor.fetchone()
            return exists > 0

        # 2. Check main table
        main_table = model_class._meta.db_table
        if not table_exists(main_table):
            return False, Response(
                {'error': f'Table "{main_table}" not found in database "{db_name}"'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. Check related tables (ForeignKey / OneToOne)
        for field in model_class._meta.get_fields():
            if isinstance(field, (ForeignKey, OneToOneField)):
                related_table = field.related_model._meta.db_table
                if not table_exists(related_table):
                    return False, Response(
                        {'error': f'Related table "{related_table}" not found in database "{db_name}"'},
                        status=status.HTTP_404_NOT_FOUND
                    )

        return True, None

    except OperationalError as e:
        return False, Response(
            {'error': f'Database error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def validate_database_and_table(db_name: str, table_name: str):
    """
    Validates that:
    1. The database exists.
    2. The specified table exists in the database.

    Returns:
        - (True, None) if all checks pass.
        - (False, Response) if any check fails (includes Response object).
    """
    if not db_name:
        return False, Response({'error': 'Missing Rty-Database header'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. Check if the database exists
        with connections['default'].cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            all_dbs = [row[0] for row in cursor.fetchall()]

        if db_name not in all_dbs:
            return False, Response({'error': f'Database {db_name} not found'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Check if the table exists in the given database
        with connections['default'].cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = %s AND table_name = %s
            """, [db_name, table_name])
            (table_exists,) = cursor.fetchone()

        if table_exists == 0:
            return False, Response({'error': f'Table {table_name} not found in {db_name}'}, status=status.HTTP_404_NOT_FOUND)

        return True, None

    except OperationalError as e:
        return False, Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


