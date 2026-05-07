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
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def notifications(request):
    print("notifications: ", request.data)
    print("request.user ======> ", request.user)
    # take = int(request.data.get("take", 100)) #POST method
    take = int(request.query_params.get("take", 100)) #GET method

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
        return Response({"error": "Not found"}, status=404)

    row.IsRead = True
    row.save()

    return Response('This notification has been marked as read.')

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

    return Response('All notifications has been marked as read.')


# POST /api/notifications/read-all
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def read_all_notifications(request):
    updated = Notification.objects.filter(
        User=request.user,
        IsRead=False
    ).update(IsRead=True)

    return Response({
        "Message": "All notifications has been marked as read successfully",
        "updated": updated
    })


# -----------------------------------
# CLEAR ALL NOTIFICATIONS
# POST /api/notifications/clear
# -----------------------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def clear_all_notifications(request):
    user = request.user

    deleted_count, _ = Notification.objects.filter(
        User=user
    ).delete()

    return Response({
        "Message": "All notifications has been cleared successfully",
        "deleted": deleted_count
    })


# -----------------------------------
# DELETE ONE NOTIFICATION
# POST /api/notifications/delete

@api_view(["POST"])
@permission_classes([AllowAny])
def delete_notification(request):
    notif_id = request.data.get("Id") or request.query_params.get("Id")

    if not notif_id:
        return Response({"Message": "Id required"}, status=400)

    try:
        row = Notification.objects.get(
            Id=notif_id,
            User=request.user,
            IsDeleted=False
        )
    except Notification.DoesNotExist:
        return Response({"Message": "Notification not found"}, status=404)

    # row.delete()
    row.IsDeleted = True
    row.save()
# Notification.objects.filter(User=request.user, IsDeleted=False) Then filter everywhere:
    return Response({"Message": "Notification has been deleted successfully"})