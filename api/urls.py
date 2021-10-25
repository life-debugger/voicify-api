
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view),
    path('signup', views.signup_view),
    path('upload_post', views.upload_new_post),
    path('latest_post', views.get_latest_post),
    path('last_five_posts', views.get_five_posts),
    path('get_user', views.get_user),
    path('update_user', views.update_user),
]