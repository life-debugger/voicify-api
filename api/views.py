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
    try:
        title = request.POST['title']
        voice = request.FILES['voice']
        username = request.POST['username']
        user = accounts.models.VoicifyUser.objects.get(username=username)
        post = models.Post.objects.create(title=title, voice=voice, owner=user)
        user.posts.add(post)
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
        avatar = user.avatar.url if user.avatar else ""
        json_user = {
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "avatar": request.build_absolute_uri(avatar)
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


@csrf_exempt
def update_user(request):
    try:
        username = request.POST.get('username', None)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        user = get_user_model().objects.get(username=username)
        avatar = request.FILES.get('avatar', None)
        print("AVATAR:", avatar)
        print("POST:", len(request.POST))
        print("FILES:", len(request.FILES))
        print("FILE:", request.FILES.get("avatar"))
        if name:
            user.name = name
        if email:
            user.email = email
        if avatar:
            user.avatar = avatar

        user.save()

        r = {
            'status': 'success',
            'msg': 'profile was updated successfully'
        }

    except Exception as e:
        r = {
            'status': 'fail',
            'msg': 'something went wrong please try again later'
        }
        raise e

    return JsonResponse(r)
