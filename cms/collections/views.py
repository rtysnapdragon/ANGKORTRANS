# apps/collections/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class SaveArtworkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, artwork_id):
        artwork = Artwork.objects.get(id=artwork_id)

        Save.objects.get_or_create(
            User=request.user,
            Artwork=artwork
        )

        if artwork.Artist != request.user:
            send_user_notification(
                artwork.Artist,
                {
                    "Type": "save",
                    "Message": f"{request.user.username} saved your artwork",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            )

        return Response({"ok": True})