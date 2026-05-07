from django.urls import path
from .views import database_list

urlpatterns = [
    path('api/databases/list', database_list, name='list-database'),
]