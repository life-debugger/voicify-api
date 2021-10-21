from django.contrib.auth import get_user_model, authenticate
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import accounts.models
from api import models


@csrf_exempt
def upload_new_post(request):
    print(request.POST)
    print(request.FILES)

    title = request.POST['title']
    voice = request.FILES['voice']
    try:
        models.Post.objects.create(title=title, voice=voice)
        return JsonResponse(
            {
                'status': 'success',
                'msg': 'Your post was uploaded successfully',
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                'status': 'fail',
                'msg': 'something went wrong',
            })


def get_latest_post(request):
    post = models.Post.objects.last()
    r = {'title': post.title, 'voice': request.build_absolute_uri(post.voice.url)}
    return JsonResponse(r)


def get_five_posts(request):
    posts = models.Post.objects.all()
    last_five_posts = posts[len(posts) - 3:]
    posts = []
    for p in last_five_posts:
        r = {'postID': p.id, 'title': p.title, 'voice': request.build_absolute_uri(p.voice.url)}
        posts.append(r)

    return JsonResponse({'posts': posts})


def login_view(request):
    return HttpResponse("login view")


@csrf_exempt
def signup_view(request):
    print(request.POST)
    get_user_model().objects.create_user(
        username=request.POST['username'],
        email=request.POST['email'],
        name=request.POST['name'],
        password=request.POST['password'],
    )

    return HttpResponse("signup view")


@csrf_exempt
def login_view(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        return JsonResponse(
            {
                'status': 'success',
                'msg': 'Login was successful',
                'user': user.username,
            }
        )
    else:
        return JsonResponse(
            {
                'status': 'fail',
                'msg': 'username or password was wrong',
            })


@csrf_exempt
def get_user(request):
    username = request.POST['username']
    try:
        user = accounts.models.VoicifyUser.objects.get(username=username)
        json_user = {
            "username": user.username,
            "name": user.name,
            "email": user.email
        }
        r = {
            'status': 'success',
            'msg': 'the user with {} username was found'.format(username),
            'user': json_user
        }

    except accounts.models.VoicifyUser.DoesNotExist as e:
        r = {
            'status': 'fail',
            'msg': 'the user with {} username was not found'.format(username),
        }

    return JsonResponse(r)
