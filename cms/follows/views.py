# apps/follows/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class FollowArtistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, artist_id):
        artist = User.objects.get(id=artist_id)

        Follow.objects.get_or_create(
            User=request.user,
            Target=artist
        )

        if artist != request.user:
            send_user_notification(
                artist,
                {
                    "Type": "follow",
                    "Message": f"{request.user.username} started following you",
                    "Href": f"/artists/{artist.username}"
                }
            )

        return Response({"ok": True})