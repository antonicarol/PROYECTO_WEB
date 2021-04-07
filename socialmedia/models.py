from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.postgres.fields import ArrayField


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profileUsername = models.CharField(max_length=20)
    email = models.CharField(max_length=20, null=True)
    firstname = models.CharField(max_length=20, null=True)
    lastname = models.CharField(max_length=20, null=True)
    lastLogin = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    content = models.CharField(max_length=120)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.content


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    startedFollowingAt = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.follower.username + " -->  " + self.to.user.username


class Image(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    userProfile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
