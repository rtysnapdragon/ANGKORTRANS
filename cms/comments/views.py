# apps/comments/views.py

from rest_framework.permissions import IsAuthenticated
from cms.artworks.models import Artwork
from cms.comments.models import Comment
from apps.notifications.services import send_user_notification
from rest_framework.response import Response

def comment(request):
    # permission_classes = [IsAuthenticated]
    if request.method == 'POST':
        artwork = Artwork.objects.get(id=request.data["ArtworkId"])
        comment = Comment.objects.create(
            Artwork=artwork,
            User=request.user,
            Message=request.data["Message"],
            Type=request.data.get('type'),
            ParentCommentId=request.data.get('parent_comment_id'),
            ReplyId=request.data.get('reply_id'),
            TotalReplies=request.data.get('total_replies'),
            TotalLikes=request.data.get('total_likes'),
            TotalDislikes=request.data.get('total_dislikes'),
            CreatedBy=request.user,
            UpdatedBy=request.user,
        )
        
        if artwork.Artist != request.user:
            send_user_notification(
                artwork.Artist,
                {
                    "Type": "comment",
                    "Message": f"{request.user.UserName} commented on \"{artwork.Title}\"",
                    "Href": f"/gallery/{artwork.Slug}"
                }
            )

        return Response({"ok": True})