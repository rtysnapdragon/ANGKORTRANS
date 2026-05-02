# apps/collections/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from cms.artworks.models import Artwork
from cms.collections.models import Save,Share,View
from apps.notifications.services import send_user_notification
from rest_framework.response import Response
from rest_framework.decorators import api_view
def save(request):
    # permission_classes = [IsAuthenticated]
    if request.method == 'POST':
        artwork = Artwork.objects.get(Id=request.data["ArtworkId"])
        save,created = Save.objects.get_or_create(
            User=request.user,
            Artwork=artwork,
            Collection=None
        )

        if created:
            artwork.Saves += 1
            artwork.save()
            send_user_notification(
                artwork.Artist,
               request.user,
                {
                    "Type": "save",
                    "Message": f"{request.user.USERNAME} saved your artwork {artwork.Title}",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            )

        return Response({"ok": True})

def like(request):
    if request.method == "POST":
        artwork = Artwork.objects.get(Id=request.POST["ArtworkId"])
        like,created = Like.objects.get_or_create(
            User=request.user,
            Artwork=artwork,
            Collection=None
        )

        if created:
            artwork.Likes += 1
            artwork.save()
            send_user_notification(
                # artwork.Artist,
               request.user,
                {
                    "Type": "like",
                    "Message": f"{request.user.USERNAME} liked your artwork {artwork.Title}",
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
            # artwork.Artist,
            request.user,
            {
                "Type": "share",
                "Message": f"{request.user.USERNAME} shared your artwork {artwork.Title}",
                "Href": f"/gallery/{artwork.Slug}"
            }
        )

        return Response({"ok": True})

@api_view(['POST'])
def view(request):
    if request.method == 'POST':
        artwork = Artwork.objects.get(Id=request.data["ArtworkId"])
        # view = View.objects.create(
        #     User=request.user,
        #     Artwork=artwork,
        #     Collection=None
        # )

        # artwork.Views += 1
        # artwork.save()
        
        send_user_notification(
            # artwork.Artist,
            request.user,
            {
                "Type": "view",
                "Message": f"{request.user.USERNAME} view your artwork {artwork.Title}",
                "Href": f"/gallery/{artwork.Slug}"
            }
        )

        return Response({"ok": True})


