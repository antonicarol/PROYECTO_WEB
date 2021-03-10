from django.shortcuts import render
from django.http import HttpRequest

from .models import Post
# Create your views here.

## CRUD -- Create, Retrieve, Update, Delete

def post_list_view(request:HttpRequest):
    post_objs = Post.objects.all()
    context = {
        'postlist' : post_objs,
    }
    return render(request, 'blog/index.html', context)