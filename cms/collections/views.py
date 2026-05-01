# apps/collections/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from cms.artworks.models import Artwork
from cms.collections.models import Save
from apps.notifications.services import send_user_notification
from rest_framework.response import Response
from rest_framework.decorators import api_view
def save(request):
    # permission_classes = [IsAuthenticated]
    if request.method == 'POST':
        artwork = Artwork.objects.get(id=request.data["ArtworkId"])
        save,created = Save.objects.get_or_create(
            User=request.user,
            Artwork=artwork
        )

        if created:
            artwork.Saves += 1
            artwork.save()
            send_user_notification(
                artwork.Artist,
                {
                    "Type": "save",
                    "Message": f"{request.user.username} saved your artwork",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            )

        return Response({"ok": True})

def like(request):
    if request.method == "POST":
        artwork = Artwork.objects.get(id=request.POST["ArtworkId"])
        like,created = Like.objects.get_or_create(
            User=request.user,
            Artwork=artwork
        )

        if created:
            artwork.Likes += 1
            artwork.save()
            send_user_notification(
                artwork.Artist,
                {
                    "Type": "like",
                    "Message": f"{request.user.username} liked your artwork",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            )

        return Response({"ok": True})


def share(request):
    if request.method == 'POST':
        artwork = Artwork.objects.get(id=request.data["ArtworkId"])
        share = Share.objects.create(
            User=request.user,
            Artwork=artwork
        )

        artwork.Shares += 1
        artwork.save()
        send_user_notification(
            artwork.Artist,
            {
                "Type": "share",
                "Message": f"{request.user.username} shared your artwork",
                "Href": f"/gallery/{artwork.Slug}"
            }
        )

        return Response({"ok": True})

@api_view(['POST'])
def view(request):
    if request.method == 'POST':
        artwork = Artwork.objects.get(id=request.data["ArtworkId"])
        view = View.objects.create(
            User=request.user,
            Artwork=artwork
        )

        artwork.Views += 1
        artwork.save()

        return Response({"ok": True})


