from django.contrib import admin
from .models import Post, UserProfile, Follow
# Register your models here.


admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Follow)