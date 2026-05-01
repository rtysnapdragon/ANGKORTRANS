from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    Id = models.AutoField(primary_key=True,db_column="ID")
    Type = models.CharField(max_length=50,db_column="TYPE")
    Message = models.TextField(db_column="MESSAGE")
    IsRead = models.BooleanField(default=False,db_column="ISREAD")
    Href = models.CharField(max_length=255,null=True,blank=True,db_column="HREF")

    User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_user_id",
        db_column="USER_ID"
    )

    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,db_column="CREATED_BY", related_name="notifications_created_by",blank=True,null=True)
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,db_column="UPDATED_BY",related_name="notifications_updated_by",blank=True,null=True)
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    IsSent = models.BooleanField(default=False,db_column="IS_SENT")
    
    class Meta:
        db_table = "NOTIFICATIONS"
        verbose_name_plural = "Notifications"
        
    def __str__(self):
        return f"{self.Id} - {self.Type}"