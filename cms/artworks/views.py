from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from .models import *
from apps.notifications.services import send_user_notification
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from rest_framework.response import Response
from cms.utils.handle import apply_request_filters
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status


from .serializers import ArtworkSerializer

@api_view(['POST'])
def list_artworks(request):
    artworks = apply_request_filters(Artwork.objects.all(), request)

    serializer = ArtworkSerializer(
        artworks,
        many=True,
        context={'request': request}
    )

    return Response(serializer.data)

@api_view(['POST'])
def create_artwork(request):
    if request.method == 'POST':
        artwork = Artwork.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            image=request.FILES['image'],
            artist=request.user,
            likes=0,
            views=0,
            saves=0,
            is_public=True,
            created_by=request.user,
            updated_by=request.user,
        )
        artwork.save()
        return Response({'status':'success'})

@api_view(['POST'])
def update_artwork(request,artwork_id):
    if request.method == 'POST':
        artwork = Artwork.objects.get(id=artwork_id)
        artwork.title=request.POST['title']
        artwork.description=request.POST['description']
        artwork.image=request.FILES['image']
        artwork.artist=request.user
        artwork.likes=0
        artwork.views=0
        artwork.saves=0
        artwork.is_public=True
        artwork.created_by=request.user
        artwork.updated_by=request.user
        artwork.save()
        return Response({'status':'success'})

@api_view(['GET'])
def delete_artwork(request,artwork_id):
    if request.method == 'GET':
        artwork = Artwork.objects.get(id=artwork_id)
        artwork.delete()
        return Response({'status':'success'})

@api_view(['POST'])
def get_artwork(request):
    artworks = Artwork.objects.all()
    
    data = []
    for artwork in artworks:
        data.append({
            'Id': artwork.Id,
            'Title': artwork.Title,
            'Slug': artwork.Slug,
            'Description': artwork.Description,
            'Image': artwork.Image.url,
            'Artist': artwork.Artist.USERNAME,
            'Likes': artwork.Likes,
            'Views': artwork.Views,
            'Saves': artwork.Saves,
            'IsPublic': artwork.IsPublic,
            'CreatedAt': artwork.CreatedAt,
            'UpdatedAt': artwork.UpdatedAt,
            'CreatedBy': artwork.CreatedBy.USERNAME,
            'UpdatedBy': artwork.UpdatedBy.USERNAME,
        })
    return Response({'status':'success', 'data':data})

@api_view(['POST'])
def get_artwork_detail(request):
    artwork_id = request.data.get('Id')
    slug = request.data.get('Slug')

    artwork = None

    if artwork_id:
        artwork = get_object_or_404(Artwork, Id=artwork_id)

    elif slug:
        artwork = get_object_or_404(Artwork, Slug=slug)

    else:
        return Response(
            {"error": "Id or Slug required"},
            status=400
        )

    return Response({
        'Id': artwork.Id,
        'Title': artwork.Title,
        'Slug': artwork.Slug,
        'Description': artwork.Description,
        'Image': artwork.Image.url,
        'Artist': artwork.Artist.USERNAME,
        'Likes': artwork.Likes,
        'Views': artwork.Views,
        'Saves': artwork.Saves,
        'IsPublic': artwork.IsPublic,
        'CreatedAt': artwork.CreatedAt,
    })

@api_view(['POST'])
def get_artwork_by_slug(request):
    if request.method == 'POST':
        artwork = Artwork.objects.get(Slug=request.POST['Slug'])

    data = {
        'Id': artwork.Id,
        'Title': artwork.Title,
        'Slug': artwork.Slug,
        'Description': artwork.Description,
        'Image': artwork.Image.url,
        'Artist': artwork.Artist.USERNAME,
        'Likes': artwork.Likes,
        'Views': artwork.Views,
        'Saves': artwork.Saves,
        'IsPublic': artwork.IsPublic,
        'CreatedAt': artwork.CreatedAt,
    }

    return Response(data)

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
                    "Message": f"{request.user.USERNAME} liked your artwork",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            }
        )

        return Response({"ok": True})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def like_artwork(request):
    artwork_id = request.data.get('ArtworkId')
    print("like_artwork: ======> ", request.user)
    if not artwork_id:
        return Response(
            {"error": "ArtworkId required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    artwork = get_object_or_404(Artwork, Id=artwork_id)

    if artwork.Artist == request.user:
        return Response({"ok": True})

    artwork.Likes += 1
    artwork.save(update_fields=['Likes'])

    print("send_user_notification artworks: ======> ", artwork.Artist, request.user)
    send_user_notification(
        # artwork.Artist,
        request.user,
        {
            "Type": "like",
            "Message": f'{request.user.USERNAME} liked your artwork "{artwork.Title}"',
            "Href": f"/gallery/{artwork.Slug}"
        }
    )

    return Response({"ok": True})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def save_artwork(request):
    artwork_id = request.data.get('ArtworkId')

    if not artwork_id:
        return Response({"error": "ArtworkId required"}, status=400)

    artwork = get_object_or_404(Artwork, Id=artwork_id)

    if artwork.Artist != request.user:
        artwork.Saves += 1
        artwork.save(update_fields=['Saves'])
        send_user_notification(
            # artwork.Artist,
            request.user,
            {
                "Type": "save",
                "Message": f'{request.user.USERNAME} saved your artwork "{artwork.Title}"',
                "Href": f"/gallery/{artwork.Slug}"
            }
        )

    return Response({"ok": True})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def share_artwork(request):
    artwork_id = request.data.get('ArtworkId')

    if not artwork_id:
        return Response({"error": "ArtworkId required"}, status=400)

    artwork = get_object_or_404(Artwork, Id=artwork_id)

    artwork.Shares += 1
    artwork.save(update_fields=['Shares'])

    if artwork.Artist != request.user:
        send_user_notification(
            artwork.Artist,
            {
                "Type": "share",
                "Message": f'{request.user.USERNAME} shared your artwork "{artwork.Title}"',
                "Href": f"/gallery/{artwork.Slug}"
            }
        )

    return Response({"ok": True})