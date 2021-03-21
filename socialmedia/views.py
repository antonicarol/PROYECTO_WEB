from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import EditProfileForm, LoginForm, NewPostForm, RegisterForm
from .utils import checkPasswordMatches, checkPasswordSecurity

from django.contrib.auth.decorators import login_required
from .models import Post, Follow, UserProfile


# Create your views here.


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if(signUpUser(**form.cleaned_data)):
                print("Something went bad!")
                return redirect('/login/')
            else:
                print("User logged in!")
                return redirect('/register/')
               
          
            
    context = {
       'form' : form 
    }
    return render(request, 'auth.html', context)

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            if(loginUser(**form.cleaned_data)):
                username = form.cleaned_data["username"]
                print("Usuario logeado")
                return redirect('/home/' + username)
            else:
                print("Este usuario no existe!")
                return redirect('/login/')

                  
          
    context = {
    }
    return render(request, 'auth.html', context)


@login_required
def home(request):
    
    if request.user.is_authenticated:
        print("User is auth")
        newPostForm = NewPostForm()
        posts = Post.objects.order_by('-timestamp')
        context = {
        'user': {
            'username':request.user.username,
            'email': request.user.email
        },
        'posts': posts,
        'newPostForm' : newPostForm
        }
        return render(request, 'home.html', context)
    else:
        return redirect('login')
       
def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = EditProfileForm(request.POST)
            if form.is_valid():
                    data = form.cleaned_data
                    user.update(username=data["username"],email=data["email"])
            
                    return redirect('/home/' + data["username"])
        
        else:
            form = EditProfileForm(initial={
            'username' : user.username,
            'email' : user.email
            })

            context = {
            'form' : form,
            'user' : user
            }
            return render(request, 'editProfile.html', context)
        
       
    else:
        redirect('login')

def userProfile(request, user):
    if request.user.is_authenticated:
        author = User.objects.get(username=user)
        posts = Post.objects.filter(author=author).order_by('-timestamp')

        userProfile = UserProfile.objects.get(user=author)
        
        followers = Follow.objects.filter(to=userProfile)
        print(followers)
        context = {
            'user': user,
            'posts' : posts,
            'followers': followers
        }
        return render(request, 'profile.html', context)
    else:
        return('login')
        
def addPost(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            author = request.user
            if content != '':
                Post.objects.create(content=content, author=author)
            return redirect('home')  
        else:
            return redirect('home')      
  






