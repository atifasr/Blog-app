
# from typing_extensions import Required
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.forms import widgets

from django.conf import settings
# Create your models here.


# class UserManager(BaseUserManager):
#     def create_user(self, first_name, last_name, username, email, password=None):
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#             first_name=first_name,
#             last_name=last_name
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_super(self, first_name, last_name, username, email, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#             password=password,
#             first_name=first_name,
#             last_name=last_name
#         )

#         user.is_active = True
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superadmin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     username = models.CharField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255, unique=True)

#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     objects = UserManager()

#     def __str__(self):
#         return self.email


# class UserManager(AbstractUserManager):
#     pass


# class User(AbstractUser):
#     objects = UserManager()


CHOICES = [("Food", "Food"),
           ('Travel', 'Travel'), ('Music', 'Music'), ('Lifestyle', 'Lifestyle'), ('Fitness', 'Fitness'), ('Sports', 'Sports')]


class Category(models.Model):
    name = models.CharField(max_length=255, choices=CHOICES)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return str(self.name)

    def get_descrip(self):
        return self.description[:30]


class topic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    article_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.article_name)


class entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    topic = models.ForeignKey(topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images', blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return " "

    # def get_like_set(self):
    #     if self.likes_set.count():
    #         return self.get_like_set.count()

    def __str__(self):
        return f'{self.text[:80]}...'


class Comment(models.Model):
    post = models.ForeignKey(entry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comment'


class likes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(entry, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'likes'


class Subscriber(models.Model):

    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"
