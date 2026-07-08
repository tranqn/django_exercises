"""Generic relations with the contenttypes framework.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/
Use when one model (Comment, Tag, Like) attaches to many other models.
"""
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    body = models.TextField()


class Article(models.Model):
    title = models.CharField(max_length=200)
    comments = GenericRelation(Comment)  # reverse access + cascade delete


# Attach a comment to any object:
#   Comment.objects.create(content_object=some_article, body="Nice!")
#   article.comments.all()
#   ct = ContentType.objects.get_for_model(Article)