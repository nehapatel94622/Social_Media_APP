from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_image', default='421-4212275_transparent-default-avatar-png-avatar-img-png-download.png')
    location = models.CharField(max_length=255)

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class FollowCount(models.Model):
    follower = models.CharField(max_length=500)
    user = models.CharField(max_length=500)
    def __str__(self):
        return self.user
   


