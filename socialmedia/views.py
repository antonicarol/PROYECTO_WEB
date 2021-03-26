from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import EditProfileForm, NewPostForm, NewUserForm, FollowUserForm,EditPostForm
from .utils import checkPasswordMatches, checkPasswordSecurity

from django.contrib.auth.decorators import login_required
from .models import Post, Follow, UserProfile

from datetime import datetime

# Create your views here.


def register(request):
    form = NewUserForm()

    context = {
       'form' : form 
    }

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            userData = form.cleaned_data
            username = userData["username"]
            # Check if user exists with that username
            user = User.objects.filter(username=username)
            if(user.__len__() > 0):
                context["error_code"] = "Usuario ya existe como " + username
                return render(request, 'register.html', context)
            
            #Check if password is secure
            password = userData["password"]
            repeatPassword = userData["repeatPassword"]


            if not checkPasswordSecurity(password):
                print("not secure")
                context["error_code"] = "Constraseña no segura, debe incluir MAYUS, minus y digito"
                return render(request, 'register.html', context)

            
            if(password != repeatPassword):
                context["error_code"] = "Las contraseñas no coinciden!"
                return render(request, 'register.html', context)
            
            # If all is ok we'll save the user
            user = User.objects.create_user(username=username, password=password)

            user.save()

            UserProfile.objects.create(user=user, profileUsername= username)

            return redirect('login')

           
    return render(request, 'register.html', context)

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
                    UserProfile.objects.filter(user= user).update( email=data["email"], firstname= data["first_name"], lastname= data["last_name"])

                    return redirect('home')
        
        else:
            userProfile = UserProfile.objects.get(user= user)
            form = EditProfileForm(
                initial= {
                    "email" : userProfile.email,
                    "first_name" : userProfile.firstname,
                    "last_name" : userProfile.lastname
                }
            )

            context = {
            'form' : form,
            'user' : user
            }
            return render(request, 'editProfile.html', context)
        
       
    else:
        redirect('login')

@login_required
def userProfile(request, user):
    if request.user.is_authenticated:
        author = User.objects.get(username=user)

        posts = Post.objects.filter(author=author).order_by('-timestamp')

        userProfile = UserProfile.objects.get(user=author)
        
        followers = Follow.objects.filter(to=userProfile).order_by('-startedFollowingAt')

        # Check if the logged user is following this user

        loggedUser = request.user

        isFollowingProfile = False
        canFollow = 1
        isOwnProfile = False

        if author.username == loggedUser.username:
            isOwnProfile = True
      
        for follower in followers:
            if follower.follower.username == loggedUser.username:
                print("is following")
                isFollowingProfile = True
                canFollow = 0

        
        followForm = FollowUserForm(
            initial={
                'username': user,
                'action' : canFollow
            }
        )
        context = {
            'user': user,
            'posts' : posts,
            'followers': followers,
            'isFollowingProfile': isFollowingProfile,
            'followUserForm': followForm,
            'isOwnProfile' : isOwnProfile
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

def editPost(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            
            content = request.POST["content"]
            timestamp = datetime.now()

            Post.objects.filter(id=post_id).update(content=content, timestamp=timestamp)

            post = Post.objects.get(id=post_id)
            return redirect('profile', post.author)
        else:

            post = Post.objects.get(id=post_id)

            form = EditPostForm(
                initial={
                    'content' : post.content
                }
            )

            context = {
                'post' : post,
                'form' : form,
            }
        return render(request, 'editPost.html', context)


def deletePost(request, post_id):
     if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            Post.objects.filter(id=post_id).delete()

            return redirect('profile', user.username)
        else:

            post = Post.objects.get(id=post_id)

            context = {
                'post' : post,
            }
        return render(request, 'deletePost.html', context)
@login_required

def follow_user(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print(request.POST)
            username = request.POST["username"]
            action = int(request.POST["action"])
            if(username is not None):
                loggedUser = request.user
                userProfile = UserProfile.objects.get(profileUsername=username)
                if action == 1:
                    #Follow
                    Follow.objects.create(follower=loggedUser, to=userProfile)

                elif action == 0:
                    #Unfollow
                    Follow.objects.filter(follower=loggedUser, to=userProfile).delete()

        return redirect('profile', username) 

  






