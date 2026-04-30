from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer

class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = Notification.objects.filter(
            User=request.user
        ).order_by('-CreatedAt')

        return Response(
            NotificationSerializer(
                rows,
                many=True
            ).data
        )

class ReadNotification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        row = Notification.objects.get(
            id=id,
            User=request.user
        )

        row.Read = True
        row.save()

        return Response({ "ok": True })

class UnreadNotificationCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            User=request.user,
            Read=False
        ).count()

        return Response({"count": count})

class ReadAll(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(
            User=request.user
        ).update(Read=True)

        return Response({ "ok": True })