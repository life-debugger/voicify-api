from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from api import models


@csrf_exempt
def index(request):
    title = 'the post title'
    voice = request.FILES['voice']
    post = models.Post.objects.create(title='new stuff', voice=voice)

    return HttpResponse("hello from api")


def get_posts():
    all_posts = models.Post.objects.all()
    for post in all_posts:
        print(post)
        print(post.title)
        print(vars(post.voice))

