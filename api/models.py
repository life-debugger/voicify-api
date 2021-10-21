from django.core.files.storage import FileSystemStorage
from django.db import models


fs = FileSystemStorage(location='voices')


class Post(models.Model):
    title = models.CharField(max_length=100)
    voice = models.FileField(upload_to='voices', default=None)
    #
    # def __str__(self):
    #     return self.title
    #
