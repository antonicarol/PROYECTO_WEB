from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import EditProfileForm, NewPostForm, NewUserForm, FollowUserForm, EditPostForm

from .utils import *

from django.contrib.auth.decorators import login_required
from .models import Post, Follow, UserProfile, Image


from django.utils import timezone
from django.db.models import Q

from django.conf import settings

from django.contrib.auth import authenticate, login


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

            userProfile = UserProfile.objects.create(
                user=user, profileUsername=username)

            # Create default image
            img = Image.objects.get(id=1)

            img.pk = None
            img.title = username
            img.userProfile = userProfile
            img.save()

            login(request, user)
            return redirect('profile', username)

    return render(request, 'registration/register.html', context)


@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        posts = getAllPosts()

        notFollowingUsers = getNotFollowingUsers(user)

        newPostForm = NewPostForm()

        # Update las login user)
        userProfile = UserProfile.objects.get(user=user)

        userImage = Image.objects.get(userProfile=userProfile)

        userProfile.lastLogin = timezone.now()

        userProfile.save()

        context = {
            'user': {
                'username': request.user.username,
            },
            'posts': posts,
            'newPostForm': newPostForm,
            'notFollowingUsers': notFollowingUsers,
            'loggedUserImage': userImage

        }
        return render(request, 'home/home.html', context)
    else:
        return redirect('login')


@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        print(request.POST)
        user = request.user
        if request.method == 'POST':
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            print(request.FILES["profileImage"])
            image = request.FILES["profileImage"]

            userProfile = UserProfile.objects.get(user=user)

            # Delete previous image
            Image.objects.get(title=user.username).delete()

            Image.objects.create(title=user.username,
                                 userProfile=userProfile, image=image)
            UserProfile.objects.filter(user=user).update(
                email=email, firstname=first_name, lastname=first_name, firstTime=True)

            return redirect('profile', user.username)


@login_required
def userProfile(request, user):
    if request.user.is_authenticated:

        author = User.objects.get(username=user)

        posts = getPostsFromAuthor(author)

        userProfile = UserProfile.objects.get(user=author)

        followers = getFollowers(userProfile)

        # Check if the logged user is following this user

        loggedUser = request.user

        isOwnProfile = checkIsOwnProfile(author, loggedUser)
        if followers.__len__() > 0:
            isFollowingProfile = checkIsFollowingUser(followers, loggedUser)
        else:
            isFollowingProfile = False

        canFollow = 0
        if isFollowingProfile:
            canFollow = 0
        else:
            canFollow = 1

        userImage = Image.objects.get(userProfile=userProfile)

        isFirstTime = False
        if(not userProfile.firstname):
            isFirstTime = True

        lastLogin = getLastLogin(userProfile)
        print(lastLogin)
        context = {
            'user': loggedUser,
            'userProfile': userProfile,
            'posts': posts,
            'followers': followers,
            'isFollowingProfile': isFollowingProfile,
            'isOwnProfile': isOwnProfile,
            'lastLogin': lastLogin,
            'userImage': userImage,
            'isFirstTime': isFirstTime,
            'loggedUserImage': userImage
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
                userProfile = UserProfile.objects.get(user=author)
                Post.objects.create(content=content, author=userProfile)
                return redirect('home')
            else:
                return redirect('home')
        else:
            return redirect('home')


def editPost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_id = int(request.POST["postId"])
            content = request.POST["content"]

            Post.objects.filter(id=post_id).update(
                content=content)

            post = Post.objects.get(id=post_id)
            return redirect('profile', post.author)


def deletePost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            post_id = request.POST["post_id"]
            Post.objects.filter(id=post_id).delete()

            return redirect('profile', user.username)


@ login_required
def follow_user(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.POST["username"]
            action = int(request.POST["action"])
            origin = request.POST["origin"]
            if(username is not None):
                if origin == "profile":
                    loggedUser = request.user
                    userProfile = UserProfile.objects.get(
                        profileUsername=username)
                    if action == 1:
                        # Follow
                        Follow.objects.create(
                            follower=loggedUser, to=userProfile)

                    elif action == 0:
                        # Unfollow
                        followerUserProfile = UserProfile.objects.get(
                            profileUsername=username)

                        Follow.objects.filter(
                            follower=loggedUser, to=followerUserProfile).delete()

                    return redirect('profile', username)
                elif origin == "ownProfile":
                    loggedUser = request.user
                    loggedUserProfile = UserProfile.objects.get(
                        profileUsername=loggedUser.username)

                    follower = User.objects.get(username=username)
                    if action == 0:
                        # Unfollow
                        Follow.objects.filter(
                            follower=loggedUser, to=loggedUserProfile).delete()
                        return redirect('profile', loggedUser.username)
                elif origin == "home":
                    loggedUser = request.user
                    u = User.objects.get(username=username)
                    userProfile = UserProfile.objects.get(
                        user=u)
                    if action == 1:
                        # Follow
                        Follow.objects.create(
                            follower=loggedUser, to=userProfile)
                    return redirect('home')
