from django.urls import path, include

urlpatterns = [
    path('', include('cms.artworks.urls')),
    path('', include('cms.comments.urls')),
    path('', include('cms.follows.urls')),
    path('', include('cms.collections.urls')),
]