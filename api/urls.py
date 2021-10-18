
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('upload_post', views.index),
    path('latest_post', views.get_latest_post),
    path('last_five_posts', views.get_five_posts),
]