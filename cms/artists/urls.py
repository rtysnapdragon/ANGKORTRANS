
from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/artist-list',artist_list,name='artist_list'),
]