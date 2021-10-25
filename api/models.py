from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    voice = models.FileField(upload_to='voices', default=None)
    owner = models.ForeignKey("accounts.VoicifyUser", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
