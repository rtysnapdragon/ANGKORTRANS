# inventory/auth/views.py   or any views file
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api_app.utils.db_connection import mysql_connection


@api_view(['POST'])
def database_list(request):
    try:
        with mysql_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT schema_name AS DatabaseName
                    FROM information_schema.schemata
                    WHERE schema_name NOT IN (
                        'information_schema',
                        'mysql',
                        'performance_schema',
                        'sys'
                    )
                    ORDER BY schema_name
                """)

                databases = [row["DatabaseName"] for row in cursor.fetchall()]

        return Response({
            "Message": "Databases retrieved successfully",
            "Databases": databases,
            "Count": len(databases)
        })

    except Exception as e:
        return Response({
            "Message": str(e)
        }, status=500)