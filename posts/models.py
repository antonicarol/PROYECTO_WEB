from django.db import models
from django.db.models.fields.related import create_many_to_many_intermediary_model

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.title + ' : '+ self.description
