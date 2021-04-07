from django.contrib import admin
from .models import Post, UserProfile, Follow, Image
# Register your models here.


admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Image)
