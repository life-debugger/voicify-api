from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from api import models


@csrf_exempt
def index(request):
    title = 'the post title'
    voice = request.FILES['voice']
    post = models.Post.objects.create(title='new stuff', voice=voice)

    return HttpResponse("hello from api")


def get_latest_post(request):
    post = models.Post.objects.last()
    r = {'title': post.title, 'voice': request.build_absolute_uri(post.voice.url)}
    return JsonResponse(r)


def get_five_posts(request):
    posts = models.Post.objects.all()
    last_five_posts = posts[len(posts)-3:]
    posts = []
    for p in last_five_posts:
        r = {'postID': p.id, 'title': p.title, 'voice': request.build_absolute_uri(p.voice.url)}
        posts.append(r)

    return JsonResponse({'posts': posts})


def get_posts():
    all_posts = models.Post.objects.all()
    for post in all_posts:
        print(post)
        print(post.title)
        print(vars(post.voice))

