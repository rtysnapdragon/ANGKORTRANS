from django.urls import path
from .views import *

urlpatterns = [
    path("api/v1/artworks", list_artworks, name="list_artworks"),
    path("api/v1/artwork/like", like_artwork, name="like_artwork"),
    path("api/v1/artwork/save", save_artwork, name="save_artwork"),
    path("api/v1/artwork/share", share_artwork, name="share_artwork"),
    path("api/v1/artwork/detail", get_artwork_detail, name="get_artwork_detail"),
    path("api/v1/artwork/detail/slug", get_artwork_by_slug, name="get_artwork_by_slug"),
]