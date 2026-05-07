from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    CREATED_BY = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_created"
    )
    CREATED_AT = models.DateTimeField(auto_now_add=True)

    UPDATED_BY = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated"
    )
    UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True