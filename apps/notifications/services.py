from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification

def send_user_notification1(user_id, payload):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "notify",
            "data": payload
        }
    )


def send_user_notification(user, payload):
    """
    user = User object
    payload = {
      Type,
      Message,
      Href
    }
    """
    print("send_user_notification: ======> ", user, payload)
    # Save DB history
    row = Notification.objects.create(
        User=user,
        Type=payload["Type"],
        Message=payload["Message"],
        Href=payload.get("Href"),
        IsRead=False
    )

    # Push realtime
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.ID}",
        {
            # "type": "notify",
            "type": "send_notification",
            "data": {
                "Id": row.Id,
                "Type": row.Type,
                "Message": row.Message,
                "Href": row.Href,
                "IsRead": row.IsRead,
                "CreatedAt": row.CreatedAt.isoformat()
            }
        }
    )

""" Uage
This is the most scalable option.

send_user_notification(
    artwork.Artist.id,
    {
        "Type": "like",
        "Message": "Someone liked your artwork",
        "Href": "/gallery/sunset-angkor"
    }
)
"""