# cms/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from cms.artworks.models import Artwork
from apps.notifications.services import send_user_notification

class FeatureArtworkView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, artwork_id):
        artwork = Artwork.objects.get(id=artwork_id)
        artwork.Featured = True
        artwork.save()

        send_user_notification(
            artwork.Artist,
            {
                "Type": "system",
                "Message": f"Your artwork \"{artwork.Title}\" has been featured.",
                "Href": f"/gallery/{artwork.Slug}"
            }
        )

        return Response({"ok": True})