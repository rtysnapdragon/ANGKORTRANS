
from django.db import models
from cms.artworks.models import Artwork
from django.conf import settings

class Content(models.Model):
    class Meta:
        db_table = "CONTENTS"

    ID = models.BigAutoField(primary_key=True)

    TITLE = models.CharField(max_length=255)
    DESCRIPTION = models.TextField()

    CONTENT_TYPE = models.CharField(max_length=50)

    VIEW_COUNT = models.BigIntegerField(default=0)

    CREATED_AT = models.DateTimeField(auto_now_add=True)