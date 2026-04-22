from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Anime(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    anime_name = models.CharField(max_length=100)
    anime_description = models.TextField()
    anime_image = models.ImageField(upload_to='anime')
    