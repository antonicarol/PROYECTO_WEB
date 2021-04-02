"""testproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from socialmedia.views import register, home, edit_profile, addPost, userProfile, follow_user, editPost, deletePost

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home, name="home"),


    # region User Proile
    path('profile/<str:user>', userProfile, name="profile"),
    path('profile/edit/', edit_profile, name="editProfile"),
    path('followUser/', follow_user, name="followUser"),
    # endregion

    path('addPost/', addPost, name="addPost"),
    path('editPost/<int:post_id>', editPost, name="editPost"),
    path('deletePost/<int:post_id>', deletePost, name="deletePost")


]
