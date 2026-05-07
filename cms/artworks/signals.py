from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    if not created:
        return

    artwork = instance.Artwork
    user = instance.User

    channel_layer = get_channel_layer()
    print("Channel Layer", channel_layer)
    print("User", user)
    print("Artwork", artwork)
    print("Artwork ID", artwork.Artist.id)
    print("User ID", user.id)
    print("Type", "like")
    print("Message", f"{user.username} liked your artwork")
    print("Href", f"/gallery/{artwork.Slug}")

    async_to_sync(channel_layer.group_send)(
        f"user_{artwork.Artist.id}",
        {
            "type": "notify",
            "data": {
                "Type": "like",
                "Message": f"{user.username} liked your artwork",
                "Href": f"/gallery/{artwork.Slug}"
            }
        }
    ) 