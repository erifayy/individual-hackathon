from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from account.models import MyUser


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Article(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to="articles/")
    added = models.DateTimeField(auto_now_add=True)
    year = models.PositiveIntegerField(null=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.body[:20]}"


class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='rating')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(default=0)
