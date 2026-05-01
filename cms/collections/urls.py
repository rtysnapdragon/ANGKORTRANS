from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/artwork/like', like, name='like'),
    path('api/v1/artwork/save', save, name='save'),
    path('api/v1/artwork/share', share, name='share'),
    path('api/v1/artwork/view', view, name='view'),
]