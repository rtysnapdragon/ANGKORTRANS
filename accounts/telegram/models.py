from django.db import models

from django.conf import settings

class UserTelegram(models.Model):

    id = models.AutoField(
        primary_key=True, 
        db_column="ID"
    )
    
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_telegram_user_id',
        db_column="USER_ID"
    )

    telegram_id = models.IntegerField(
        unique=True,
        null=True,
        db_column="TELEGRAM_ID",
        blank=True
    )

    username = models.CharField(
        max_length=255,
        null=True,
        db_column="USERNAME",
        blank=True
    )

    avatar = models.URLField(
        null=True,
        db_column="AVATAR",
        blank=True
    )

    first_name = models.CharField(
        max_length=255,
        null=True,
        db_column="FIRST_NAME",
        blank=True
    )
    
    last_name = models.CharField(
        max_length=255,
        null=True,
        db_column="LAST_NAME",
        blank=True
    )
    
    phone_number = models.CharField(
        max_length=255,
        null=True,
        db_column="PHONE_NUMBER",
        blank=True
    )
    
    email = models.CharField(
        max_length=255,
        null=True,
        db_column="EMAIL",
        blank=True
    )
    
    auth_date = models.BigIntegerField(
        null=True,
        db_column="AUTH_DATE",
        blank=True
    )
    
    joined_at = models.DateTimeField(
        null=True,
        db_column="JOINED_AT",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column="CREATED_AT"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        db_column="UPDATED_AT"
    )

    class Meta:
        db_table = 'USERTELEGRAM'
        verbose_name = 'User Telegram'
        verbose_name_plural = 'User Telegrams'

    def __str__(self):
        return self.telegram_username or str(self.telegram_id)