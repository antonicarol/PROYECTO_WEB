import re
from django.contrib.auth.models import User
from .models import Post, Follow, UserProfile
from django.db.models import Q
from django.utils import timezone

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


# region posts

def getPostsFromAuthor(author):
    posts = Post.objects.filter(author=author).order_by('-timestamp')

    formattedPosts = []

    for post in posts:
        timestamp = post.timestamp
        postedAt = getTimeInterval(timestamp)

        formattedPosts.append({
            'author': post.author,
            'timestamp': postedAt,
            'content': post.content,
            'id': post.id
        })

    return formattedPosts


def getAllPosts():
    posts = Post.objects.filter().order_by('-timestamp')

    formattedPosts = []

    for post in posts:
        timestamp = post.timestamp
        postedAt = getTimeInterval(timestamp)
        formattedPosts.append({
            'author': post.author,
            'timestamp': postedAt,
            'content': post.content,
            'id': post.id
        })

    return formattedPosts


def getTimeInterval(timestamp):

    interval = (timezone.now() - timestamp).__str__()

    if interval.__len__() > 15:
        if interval.__len__() <= 23:
            days = interval[0]
            if int(days) == 1:
                return days + " day ago"
            else:
                return days + " days ago"
        else:
            months = interval[0]
            if int(months) == 1:
                return months + " month ago"
            else:
                return months + " months ago"
    else:
        (hours, minutes, seconds) = interval.__str__().split(":")

        if int(hours) > 0:
            hours = hours.replace('0', '', 1)
            if int(hours == 1):
                return hours + " hour ago"
            else:
                return hours + " hours ago"

        minutes = minutes.replace('0', '', 1)
        if int(minutes) > 0:
            if int(minutes == 1):
                return minutes + " minut ago"
            else:
                return minutes + " minutes ago"

        n_seconds = round(float(seconds), 2)

        if int(n_seconds) == 0:
            seconds = int(n_seconds)
            return "Right now"
        else:
            seconds = int(n_seconds)
            return str(seconds) + " seconds ago"


# endregion


def getLastLogin(userProfile):
    lastLogin = userProfile.lastLogin

    interval = (timezone.now() - lastLogin).__str__()

    if interval.__len__() > 15:
        if interval.__len__() <= 23:
            days = interval[0]
            if int(days) == 1:
                return days + " day ago"
            else:
                return days + " days ago"
        else:
            months = interval[0]
            if int(months) == 1:
                return months + " month ago"
            else:
                return months + " months ago"
    else:
        (hours, minutes, seconds) = interval.__str__().split(":")

        if int(hours) > 0:
            hours = hours.replace('0', '', 1)
            if int(hours == 1):
                return hours + " hour ago"
            else:
                return hours + " hours ago"

        minutes = minutes.replace('0', '', 1)
        if int(minutes) > 0:
            if int(minutes == 1):
                return minutes + " minut ago"
            else:
                return minutes + " minutes ago"

        n_seconds = round(float(seconds), 2)

        if int(n_seconds) == 0:
            seconds = int(n_seconds)
            return "Right now"
        else:
            seconds = int(n_seconds)
            return str(seconds) + " seconds ago"
