# apps/comments/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, artwork_id):
        artwork = Artwork.objects.get(id=artwork_id)

        Comment.objects.create(
            Artwork=artwork,
            User=request.user,
            Message=request.data["Message"]
        )

        if artwork.Artist != request.user:
            send_user_notification(
                artwork.Artist,
                {
                    "Type": "comment",
                    "Message": f"{request.user.username} commented on \"{artwork.Title}\"",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            )

        return Response({"ok": True})