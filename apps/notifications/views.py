from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status


from .models import Notification
from .serializers import NotificationSerializer


# -----------------------------------
# LIST NOTIFICATIONS
# GET /api/notifications?take=100
# -----------------------------------
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def notifications(request):
    print("notifications: ", request.data)
    print("request.user ======> ", request.user)
    take = int(request.data.get("take", 100))

    rows = Notification.objects.filter(
        User=request.user
    ).order_by("-CreatedAt")[:take]

    data = NotificationSerializer(rows, many=True).data

    return Response(data)


# -----------------------------------
# MARK ONE READ
# POST /api/notifications/read/5
# -----------------------------------
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def read_notification(request):
    Id = request.data.get("Id") or request.query_params.get("Id")

    if not Id:
        return Response(
            {"Message": "Id required"},
            status=400
        )

    try:
        row = Notification.objects.get(
            Id=Id,
            User=request.user
        )
    except Notification.DoesNotExist:
        return Response(
            {"Message": "Not found"},
            status=404
        )

    row.IsRead = True
    row.save()

    return Response({"ok": True})

# -----------------------------------
# UNREAD COUNT
# GET /api/notifications/unread-count
# -----------------------------------
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def unread_notifications_count(request):
    count = Notification.objects.filter(
        User=request.user,
        IsRead=False
    ).count()

    return Response({"count": count})


# -----------------------------------
# MARK ALL READ
# POST /api/notifications/read-all
# -----------------------------------
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def read_all(request):
    Notification.objects.filter(
        User=request.user,
        IsRead=False
    ).update(IsRead=True)

    return Response({"ok": True})