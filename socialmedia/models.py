from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    content = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.content


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)