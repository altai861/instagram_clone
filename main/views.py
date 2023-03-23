from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Profile, Activity, Post, Like, Comment, Saved, Follow
from django.http import JsonResponse
import json




def profile(request, username):
    if username == 'admin':
        return HttpResponseRedirect(reverse('admin'))
    user = User.objects.get(username=username)
    profiles = Profile.objects.all()
    if request.user == user:
        return HttpResponseRedirect(reverse('my_profile'))
    else:

        user_profile = Profile.objects.get(user=user)
        my_profile = Profile.objects.get(user=request.user)
        followed = False
        if user in my_profile.who_I_followed():
            followed = True

        posts = Post.objects.filter(user=user)
        return render(request, 'profile.html', {
            "user":user,
            "profile":user_profile,
            "posts":posts,
            "profiles":profiles,
            "followed":followed,

        })


def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    activities = Activity.objects.filter(user=request.user)
    my_posts = Post.objects.filter(user=request.user)
    saved_posts = []
    all_profiles = Profile.objects.all()
    for post in Post.objects.all():
        if request.user in post.who_saved():
            saved_posts.append(post)
    
    return render(request, 'my_profile.html', {
        "profile":profile,
        "activities":activities,
        "posts":my_posts,
        "saved_posts":saved_posts,
        "all_profiles":all_profiles
    })
# Create your views here.
def index(request):
    
    if request.user.is_authenticated:
        posts = Post.objects.all()
        profiles = Profile.objects.all()
        present_profile = Profile.objects.get(user=request.user)
    if request.user.is_authenticated:
        return render(request, 'home.html', {
            'posts':posts,
            'profiles':profiles,
            'present_profile':present_profile,
        })
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first"]
        last_name = request.POST["last"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, first_name=first_name,last_name=last_name,password=password)
            user.save()
            profile = Profile(user=user)
            profile.save()

            
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Username address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")



def activity(request):
    if request.method == 'POST':
        the_activity = request.POST['activity']
        new_activity = Activity(user=request.user, activity_name= the_activity)
        new_activity.save()
      
        return render(request, "activity.html", {
            "message": "Successfully added activity. Make sure you post some photo or video after doing that :)",
        })
        
    return render(request, 'activity.html')

def edit_profile(request):
    if request.method == "POST":
        new_username = request.POST['username']
        new_bio = request.POST['bio']
        user = request.user
        try:
            user.username = new_username
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "edit_profile.html", {
                "message": "Username address already taken."
            })
        the_profile = Profile.objects.get(user=request.user)
        the_profile.bio = new_bio
        the_profile.save()
        
        return my_profile(request)
    else:
        profile = Profile.objects.get(user=request.user)
        return render(request, "edit_profile.html", {
            "profile":profile,
        })

def edit_profile_picture(request):
    if request.method == "POST":
        photo = request.FILES['profile-picture']
        the_profile = Profile.objects.get(user=request.user)
        the_profile.profile_image.delete()
        the_profile.profile_image = photo
        the_profile.save()
        return my_profile(request)
    else:
        the_profile = Profile.objects.get(user=request.user)
        return render(request, "edit_profile_picture.html", {
            "profile":the_profile,
        })

def make_post(request):
    if request.method == "POST":
        photo = request.FILES['post-image']
        text = request.POST['post-text']
        the_activity_name = request.POST['activity_name']
        the_activity = Activity.objects.get(activity_name=the_activity_name)
        new_post = Post(user=request.user, activity=the_activity, image=photo, post_text=text)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        activities = Activity.objects.filter(user=request.user)
        return render(request, 'make_post.html', {
            "activities":activities,
        })

def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    likes = Like.objects.filter(user=request.user, post=post)
    likes.delete()
    return JsonResponse({"message":"successfully unliked"})

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    like = Like(user=request.user, post=post)
    like.save()
    return JsonResponse({"message":"successfully liked"})

def comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data['post_id']
        comment = data['comment']
        the_post = Post.objects.get(pk=post_id)
        new_comment = Comment(user=request.user, comment=comment, post=the_post)
        new_comment.save()
        return JsonResponse({"message":"Successfully commented"})
    else:
        return JsonResponse({"message":"ONLY post request required"})

    
def unsave(request, post_id):
    post = Post.objects.get(pk=post_id)
    save = Saved.objects.get(user=request.user, post=post)
    save.delete()
    return JsonResponse({"message":"successfully unsaved"})

def save(request, post_id):
    post = Post.objects.get(pk=post_id)
    save = Saved(user=request.user, post=post)
    save.save()
    return JsonResponse({"message":"successfully saved"})

def follow(request, username):
    followed_user = User.objects.get(username=username)
    new_follow = Follow(user=request.user,followed_person=followed_user)
    new_follow.save()
    return JsonResponse({"message":"successfully followed"})

def unfollow(request, username):
    followed_user = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, followed_person=followed_user).delete()
    return JsonResponse({"message":"successfully unfollowed"})