import re
from django.contrib.auth.models import User
from .models import Post, Follow, UserProfile
from django.db.models import Q
import enum


# region Login and Register
def checkPasswordMatches(paswd, repPaswd):
    if(paswd == repPaswd):
        return True
    else:
        return False


def checkPasswordSecurity(password):
    flag = 0
    while True:
        if (len(password) < 8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif re.search("\s", password):
            flag = -1
            break
        else:
            flag = 0
            return True
            break

    if flag == -1:
        return False


def checkUserExists(user):
    if user.__len__():
        return True
    else:
        return False

# endregion


# region Home

def getNotFollowingUsers(loggedUser):

    users = UserProfile.objects.filter(
        ~Q(user=loggedUser))

    notFollowingUsers = []

    for u in users:
        isFollowing = Follow.objects.filter(to=u, follower=loggedUser)
        if isFollowing.count() == 0:
            followers = 1
            notFollowingUsers.append(({
                'user': u,
                'followers': followers
            }))

    return notFollowingUsers
# endregion


# region  Profile

def checkIsOwnProfile(author, loggedUser):
    if author.username == loggedUser.username:
        return True
    else:
        return False


def checkIsFollowingUser(followers, loggedUser):
    for follower in followers:
        if follower.follower.username == loggedUser.username:
            return True
    return False
# endregion
