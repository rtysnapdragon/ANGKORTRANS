from django.urls import path
from .views import FeatureArtworkView
from cms.artworks.views import (
    LikeArtworkView
)
from cms.comments.views import (
    CreateCommentView
)
from cms.follows.views import (
    FollowArtistView
)
from cms.collections.views import (
    SaveArtworkView
)

urlpatterns = [
 path("api/artworks/like", LikeArtworkView.as_view()),
 path("api/artworks/comment", CreateCommentView.as_view()),
 path("api/artists/follow", FollowArtistView.as_view()),
 path("api/artworks/save", SaveArtworkView.as_view()),
 path("api/artworks/feature", FeatureArtworkView.as_view()),
]