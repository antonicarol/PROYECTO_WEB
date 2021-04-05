from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import EditProfileForm, NewPostForm, NewUserForm, FollowUserForm, EditPostForm

from .utils import checkPasswordMatches, checkPasswordSecurity, checkUserExists, getNotFollowingUsers, checkIsOwnProfile, checkIsFollowingUser, getPostsFromAuthor, getAllPosts

from django.contrib.auth.decorators import login_required
from .models import Post, Follow, UserProfile

from datetime import datetime
from django.db.models import Q

# Create your views here.


def register(request):
    registerform = NewUserForm()

    context = {
        'form': registerform
    }

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            userData = form.cleaned_data
            username = userData["username"]
            # Check if user exists with that username
            user = User.objects.filter(username=username)
            if checkUserExists(user):
                context["error_code"] = "Usuario ya existe como " + username
                return render(request, 'registration/register.html', context)

            # Check if password is secure
            password = userData["password"]
            repeatPassword = userData["repeatPassword"]

            if not checkPasswordSecurity(password):
                context["error_code"] = "Constraseña no segura, debe incluir MAYUS, minus y digito"
                return render(request, 'registration/register.html', context)

            if not checkPasswordMatches(password, repeatPassword):
                context["error_code"] = "Las contraseñas no coinciden!"
                return render(request, 'registration/register.html', context)

            # If all is ok we'll save the user
            user = User.objects.create_user(
                username=username, password=password)

            user.save()

            UserProfile.objects.create(user=user, profileUsername=username)

            return redirect('login')

    return render(request, 'registration/register.html', context)


@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        posts = getAllPosts()

        notFollowingUsers = getNotFollowingUsers(user)

        newPostForm = NewPostForm()

        context = {
            'user': {
                'username': request.user.username,
            },
            'posts': posts,
            'newPostForm': newPostForm,
            'notFollowingUsers': notFollowingUsers
        }
        return render(request, 'home/home.html', context)
    else:
        return redirect('login')


def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = EditProfileForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                UserProfile.objects.filter(user=user).update(
                    email=data["email"], firstname=data["first_name"], lastname=data["last_name"])

                return redirect('home')

        else:
            userProfile = UserProfile.objects.get(user=user)
            form = EditProfileForm(
                initial={
                    "email": userProfile.email,
                    "first_name": userProfile.firstname,
                    "last_name": userProfile.lastname
                }
            )

            context = {
                'form': form,
                'user': user
            }
            return render(request, 'profile/editProfile.html', context)

    else:
        redirect('login')


@ login_required
def userProfile(request, user):
    if request.user.is_authenticated:

        author = User.objects.get(username=user)

        posts = getPostsFromAuthor(author)

        userProfile = UserProfile.objects.get(user=author)

        followers = Follow.objects.filter(
            to=userProfile).order_by('-startedFollowingAt')

        # Check if the logged user is following this user

        loggedUser = request.user

        isOwnProfile = checkIsOwnProfile(author, loggedUser)

        isFollowingProfile = checkIsFollowingUser(followers, loggedUser)

        canFollow = 0
        if isFollowingProfile:
            canFollow = 0
        else:
            canFollow = 1

        followForm = FollowUserForm(
            initial={
                'username': author.username,
                'action': canFollow,
                'origin': 'profile'
            }
        )

        context = {
            'user': loggedUser,
            'userProfile': userProfile,
            'posts': posts,
            'followers': followers,
            'isFollowingProfile': isFollowingProfile,
            'followUserForm': followForm,
            'isOwnProfile': isOwnProfile
        }
        return render(request, 'profile/userProfile.html', context)
    else:
        return('login')


@ login_required
def addPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST

            content = data["content"]
            author = request.user
            if content != '':
                Post.objects.create(content=content, author=author)
                return redirect('home')
            else:
                return redirect('home')
        else:
            return redirect('home')


def editPost(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST":

            content = request.POST["content"]
            timestamp = datetime.now()

            Post.objects.filter(id=post_id).update(
                content=content, timestamp=timestamp)

            post = Post.objects.get(id=post_id)
            return redirect('profile', post.author)
        else:

            post = Post.objects.get(id=post_id)

            form = EditPostForm(
                initial={
                    'content': post.content
                }
            )

            context = {
                'post': post,
                'form': form,
            }
        return render(request, 'posts/editPost.html', context)


def deletePost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            post_id = request.POST["post_id"]
            Post.objects.filter(id=post_id).delete()

            return redirect('profile', user.username)
        else:

            post = Post.objects.get(id=post_id)

            context = {
                'post': post,
            }
        return render(request, 'posts/deletePost.html', context)


@ login_required
def follow_user(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.POST["username"]
            action = int(request.POST["action"])
            origin = request.POST["origin"]
            if(username is not None):
                loggedUser = request.user
                userProfile = UserProfile.objects.get(profileUsername=username)
                if action == 1:
                    # Follow
                    Follow.objects.create(follower=loggedUser, to=userProfile)

                elif action == 0:
                    # Unfollow
                    Follow.objects.filter(
                        follower=loggedUser, to=userProfile).delete()

                if(origin == "home"):
                    return redirect('home')
                elif(origin == "profile"):
                    return redirect('profile', username)
