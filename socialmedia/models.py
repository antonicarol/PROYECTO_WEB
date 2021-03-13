from django.db import models

# Create your models here.

class User(models.Model):
    Username = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)

    def __str__(self):
        return self.Username
    


