from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages
from .models import Profile, Post, LikePost, FollowCount
from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    
    user_following_list = []
    feed = []

    user_followinig = FollowCount.objects.filter(follower=request.user.username)

    for users in user_followinig:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))
        
    #user suggestion starts
    all_user = User.objects.all()
    user_following_all = []
    
    for user in user_followinig:
        user_lists = User.objects.get(username=user.user)
        user_following_all.append(user_lists)

    new_suggestions_list = [x for x in list(all_user) if (x not in list(user_followinig))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
    
    suggestion_user_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html',{'user_profile':user_profile,'posts':feed_list, 'final_suggestions_list':final_suggestions_list, 'suggestion_user_profile_list':suggestion_user_profile_list[:4]})

@login_required(login_url='signin')
def Search_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        username_profile_list = list(chain(*username_profile_list))
        
    return render(request, 'search.html', {'user_profile':user_profile,'username_profile_list':username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')



@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('index')

    else:
        return redirect('index')




@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profile_image
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')
        
    return render(request, 'setting.html', {'user_profile':user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                

                #Log user in and return redirect settings page
                user_login = authenticate(username=username, password=password)
                login(request, user_login)

                
                #create profile object for newuser
                user_model = User.objects.get(username=username)
                profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Password Does Not Match.')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def Profile_view(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.filter(user=pk)
    user_post_length = len(posts)

    follower = request.user.username
    user = pk

    if FollowCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    user_follower = len(FollowCount.objects.filter(user=pk))
    user_following = len(FollowCount.objects.filter(follower=pk))

    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'posts':posts,
        'user_post_length': user_post_length,
        'button_text':button_text,
        'user_follower':user_follower,
        'user_following':user_following,
      
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowCount.objects.filter(follower=follower, user=user).first():
            delete_follow = FollowCount.objects.get(follower=follower, user=user)
            delete_follow.delete()
            return redirect('/profile/'+ user)
        else:
            new_follower = FollowCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+ user)
    else:
        return redirect('index')     




