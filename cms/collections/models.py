from django.db import models
from django.conf import settings
from cms.artworks.models import Artwork

class Collection(models.Model):
    Id = models.IntegerField(auto_created=True,primary_key=True,db_column="ID")
    Name = models.CharField(max_length=255,db_column="NAME")
    Slug = models.SlugField(unique=True,db_column="SLUG")
    Description = models.TextField(db_column="DESCRIPTION")
    Image = models.ImageField(upload_to='collections/',db_column="IMAGE")
    Artist = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='collection_artist_id',db_column="ARTIST_ID")
    Artwork = models.ManyToManyField(Artwork,related_name='collection_artwork_id',db_column="ARTWORK_ID")

    Likes = models.IntegerField(default=0,db_column="LIKES")
    Views = models.IntegerField(default=0,db_column="VIEWS")
    Saves = models.IntegerField(default=0,db_column="SAVES")

    IsPublic = models.BooleanField(default=True,db_column="IS_PUBLIC")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='collection_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='collection_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")

    class Meta:
        db_table = "COLLECTIONS"
        managed = True
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

        
    def __str__(self):
        return str(self.id)

class Save(models.Model):
    Id = models.IntegerField(auto_created=True,primary_key=True,db_column="ID")
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='save_user_id',db_column="USER_ID")
    Artwork = models.ForeignKey(Artwork,on_delete=models.CASCADE,related_name='save_artwork_id',db_column="ARTWORK_ID")
    Collection = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name='save_collection_id',db_column="COLLECTION_ID")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='save_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='save_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")

    class Meta:
        db_table = "SAVES"
        managed = True
        verbose_name = "Save"
        verbose_name_plural = "Saves"

        
    def __str__(self):
        return str(self.id)

class Share(models.Model):
    Id = models.IntegerField(auto_created=True,primary_key=True,db_column="ID")
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='share_user_id',db_column="USER_ID")
    Artwork = models.ForeignKey(Artwork,on_delete=models.CASCADE,related_name='share_artwork_id',db_column="ARTWORK_ID")
    Collection = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name='share_collection_id',db_column="COLLECTION_ID")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='share_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='share_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")

    class Meta:
        db_table = "SHARES"
        managed = True
        verbose_name = "Share"
        verbose_name_plural = "Shares"

        
    def __str__(self):
        return str(self.id)

class View(models.Model):
    Id = models.IntegerField(auto_created=True,primary_key=True,db_column="ID")
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='view_user_id',db_column="USER_ID")
    Artwork = models.ForeignKey(Artwork,on_delete=models.CASCADE,related_name='view_artwork_id',db_column="ARTWORK_ID")
    Collection = models.ForeignKey(Collection,on_delete=models.CASCADE,related_name='view_collection_id',db_column="COLLECTION_ID")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='view_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='view_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")

    class Meta:
        db_table = "VIEWS"
        managed = True
        verbose_name = "View"
        verbose_name_plural = "Views"

        
    def __str__(self):
        return str(self.id)