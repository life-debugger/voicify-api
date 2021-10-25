from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from api import models as api_models


class MyUserManager(BaseUserManager):
    def create_user(self, username, name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class VoicifyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )

    posts = models.ManyToManyField(api_models.Post)
    avatar = models.ImageField(upload_to='avatars', blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'password']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
