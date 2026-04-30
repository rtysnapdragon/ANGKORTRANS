
# from accounts.users.models import Users
from django.conf import settings
from django.db import models

class Artwork(models.Model):
    Title = models.CharField(max_length=255)
    Slug = models.SlugField(unique=True)
    Description = models.TextField()
    Image = models.ImageField(upload_to='artworks/')
    Artist = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    Likes = models.IntegerField(default=0)
    Views = models.IntegerField(default=0)
    Saves = models.IntegerField(default=0)

    CreatedAt = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    Artwork = models.ForeignKey(Artwork,on_delete=models.CASCADE)
    User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Message = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)