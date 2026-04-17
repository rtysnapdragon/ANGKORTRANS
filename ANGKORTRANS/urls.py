"""
URL configuration for ANGKORTRANS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import django
from django.http import JsonResponse
from django.utils import timezone
from django.db import connection
import os
from django.conf import settings
from django.shortcuts import render
from .views import HomeView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import filter_address

# print(" Dir =-> ", os.path.join(settings.BASE_DIR, 'templates'))
def home(request):
    db_status = "OK"
    db_class = "ok"

    try:
        connection.ensure_connection()
    except Exception:
        db_status = "FAILED"
        db_class = "bad"

    context = {
        "status": "OK",
        "message": "ANGKORTRANS API Running",
        "time": timezone.now(),
        "django_version": django.get_version(),
        "db_status": db_status,
        "db_class": db_class,
    }

    return render(request, "index.html", context)

# def home(request):
#     return JsonResponse({"message": "ANGKORTRANS API is running"})

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('admin/', admin.site.urls),    
    path('',include('api_app.urls')),
    path('',include('inventory.urls')),
    path('',include('accounts.urls')),
    path('', include('admin_address.urls')),
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # This is /api/docs/
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/addresses', filter_address, name='filter_address'),
]

"""bash
4. Example API Usage
🔹 Get all provinces
GET /api/addresses
🔹 Filter by province
GET /api/addresses?province_code=01
🔹 Filter by province + district
GET /api/addresses?province_code=01&district_code=0102
🔹 Full filter
GET /api/addresses?province_code=01&district_code=0102&commune_code=010201&village_code=01020101
5. Pagination
GET /api/addresses?province_code=1&district_code=102&page=2&page_size=100

"""