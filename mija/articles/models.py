from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=50)


class Article(models.Model):
    class Meta:
        permissions = ((
            "can_publish_unpublish",
            "Can publish or unpublish articles"),
        )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    article_title = models.CharField(max_length=200)
    article_body = models.TextField()
    published = models.BooleanField(default=False)
