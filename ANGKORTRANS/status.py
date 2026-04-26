from django.shortcuts import render
from django.db import connection
from django.utils import timezone
import django

def status_page(request):
    db_status = "OK"
    db_class = "ok"

    try:
        connection.ensure_connection()
    except Exception:
        db_status = "FAILED"
        db_class = "bad"

    context = {
        "time": timezone.now(),
        "django_version": django.get_version(),
        "db_status": db_status,
        "db_class": db_class,
    }

    return render(request, "index.html", context)