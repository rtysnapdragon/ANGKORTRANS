
# from accounts.users.models import Users
from django.conf import settings
from django.db import models

class Artwork(models.Model):
    Id = models.AutoField(primary_key=True, db_column="ID")
    Title = models.CharField(max_length=255,db_column="TITLE")
    Slug = models.SlugField(unique=True,db_column="SLUG")
    Description = models.TextField(db_column="DESCRIPTION")
    Image = models.ImageField(upload_to='artworks/',db_column="IMAGE")
    Artist = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='artwork_artist_id',db_column="ARTIST_ID")

    Likes = models.IntegerField(default=0,db_column="LIKES")
    Views = models.IntegerField(default=0,db_column="VIEWS")
    Saves = models.IntegerField(default=0,db_column="SAVES")

    IsPublic = models.BooleanField(default=True,db_column="IS_PUBLIC")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='artwork_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='artwork_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")

    class Meta:
        db_table = "ARTWORKS"
        managed = True
        verbose_name = "Artwork"
        verbose_name_plural = "Artworks"

        
    def __str__(self):
        return str(self.Id)