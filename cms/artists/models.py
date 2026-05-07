from django.db import models
class Artist(models.Model):
    Id = models.AutoField(primary_key=True, db_column="ID")
    Name = models.CharField(max_length=255,db_column="NAME")
    Bio = models.TextField(db_column="BIO")
    ProfilePicture = models.ImageField(upload_to='artists/profile',db_column="PROFILE_PICTURE")
    Website = models.URLField(db_column="WEBSITE")
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='artist_created_by',db_column="CREATED_BY")
    UpdatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='artist_updated_by',db_column="UPDATED_BY")
    CreatedAt = models.DateTimeField(auto_now_add=True,db_column="CREATED_AT")
    UpdatedAt = models.DateTimeField(auto_now=True,db_column="UPDATED_AT")
    def __str__(self):
        return self.Name
    class Meta:
        db_table = "ARTISTS"
        managed = True
        verbose_name = "Artist"
        verbose_name_plural = "Artists"