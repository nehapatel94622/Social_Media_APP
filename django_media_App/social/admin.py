from django.contrib import admin
from .models import Profile, Post, LikePost, FollowCount
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("location", "profile_image", "bio", "id_user", "user", "id")[::-1]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("no_of_likes", "created_at", "caption", "image", "user", "id")[::-1]


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ("username", "post_id")[::-1]


@admin.register(FollowCount)
class FollowCountAdmin(admin.ModelAdmin):
    list_display = ("user", "follower")[::-1]
