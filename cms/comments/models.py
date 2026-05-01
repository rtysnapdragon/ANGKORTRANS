from django.db import models
from cms.artworks.models import Artwork
from django.conf import settings


class Comment(models.Model):
    Id = models.IntegerField(auto_created=True,primary_key=True,db_column="ID")
    Artwork = models.ForeignKey(Artwork,on_delete=models.CASCADE,related_name='artwork_id',db_column="ARTWORK_ID")
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comment_user_id',db_column="USER_ID")
    Message = models.TextField(db_column="MESSAGE")
    Type = models.CharField(max_length=100,db_column="TYPE")
    ParentCommentId = models.ForeignKey('self',on_delete=models.CASCADE,related_name='parent_comment_id',db_column="PARENT_COMMENT_ID",null=True,blank=True)
    ReplyId = models.ForeignKey('self',on_delete=models.CASCADE,related_name='reply_id',db_column="REPLY_ID",null=True,blank=True)
    TotalReplies = models.IntegerField(default=0,db_column="TOTAL_REPLIES")
    TotalLikes = models.IntegerField(default=0,db_column="TOTAL_LIKES")
    TotalDislikes = models.IntegerField(default=0,db_column="TOTAL_DISLIKES")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comment_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comment_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")

    def __str__(self):
        return str(self.Id)
    
    class Meta:
        db_table = "COMMENTS"
        managed = True
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    


class Reply(models.Model):
    Id = models.IntegerField(auto_created=True,primary_key=True,db_column="ID")
    Artwork = models.ForeignKey(Artwork,on_delete=models.CASCADE,related_name='reply_artwork_id',db_column="ARTWORK_ID")
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reply_user_id',db_column="USER_ID")
    Message = models.TextField(db_column="MESSAGE")
    Type = models.CharField(max_length=100,db_column="TYPE")
    ParentCommentId = models.ForeignKey('self',on_delete=models.CASCADE,related_name='reply_parent_comment_id',db_column="PARENT_COMMENT_ID",null=True,blank=True)
    ReplyId = models.ForeignKey('self',on_delete=models.CASCADE,related_name='reply_reply_id',db_column="REPLY_ID",null=True,blank=True)
    TotalReplies = models.IntegerField(default=0,db_column="TOTAL_REPLIES")
    TotalLikes = models.IntegerField(default=0,db_column="TOTAL_LIKES")
    TotalDislikes = models.IntegerField(default=0,db_column="TOTAL_DISLIKES")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reply_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reply_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")

    def __str__(self):
        return str(self.Id)
    
    class Meta:
        db_table = "REPLIES"
        managed = True
        verbose_name = "Reply"
        verbose_name_plural = "Replies"
