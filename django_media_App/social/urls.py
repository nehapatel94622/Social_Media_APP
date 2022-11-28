from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('like-post/', views.like_post, name='like-post'),
    path('profile/<str:pk>/', views.Profile_view, name='profile'),
    path('follow/', views.follow, name='follow'),
    path('search/', views.Search_view, name='search'),

]
