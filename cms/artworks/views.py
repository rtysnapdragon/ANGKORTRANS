from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from .models import *
from apps.notifications.services import send_user_notification
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def ArtworkView(request):
    Artwork = request.data.get('Artwork')
    IP = request.data.get('IP')
    ArtworkView.objects.create(Artwork=Artwork,IP=IP)
    Artwork.views += 1
    Artwork.save()
    return Response({'status':'success'})


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from rest_framework.response import Response

class LikeArtworkView11(APIView):
    def post(self, request, artwork_id):
        artwork = Artwork.objects.get(id=artwork_id)

        # save like logic here
        artwork.Likes += 1
        artwork.save()

        # notify artwork owner
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"user_{artwork.Artist.id}",
            {
                "type": "notify",
                "data": {
                    "Type": "like",
                    "Message": f"{request.user.username} liked your artwork",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            }
        )

        return Response({"ok": True})


class LikeArtworkView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, artwork_id):
        artwork = Artwork.objects.get(id=artwork_id)

        artwork.Likes += 1
        artwork.save()

        if artwork.Artist != request.user:
            send_user_notification(
                artwork.Artist,
                {
                    "Type": "like",
                    "Message": f"{request.user.username} liked your artwork \"{artwork.Title}\"",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            )

        return Response({"ok": True})