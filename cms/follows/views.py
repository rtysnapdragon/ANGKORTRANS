# apps/follows/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

def follow(request):
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


def unfollow(request):
    permission_classes = [IsAuthenticated]

    def post(self, request, artist_id):
        artist = User.objects.get(id=artist_id)

        Follow.objects.filter(
            User=request.user,
            Target=artist
        ).delete()

        return Response({"ok": True})


def follower(request):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(id=request.data["UserId"])
        followers = Follow.objects.filter(Target=user)
        return Response({"followers": followers})


def following(request):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(id=request.data["UserId"])
        following = Follow.objects.filter(User=user)
        return Response({"following": following})


def follow_status(request):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(id=request.data["UserId"])
        artist = User.objects.get(id=request.data["ArtistId"])
        follow_status = Follow.objects.filter(User=user, Target=artist).exists()
        return Response({"follow_status": follow_status})