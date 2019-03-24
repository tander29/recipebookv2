from django.db import models
from django.contrib.auth.models import User

"""Models for this django application"""


class Author(models.Model):
    name = models.TextField()
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(
        'Recipe', related_name='favorites', blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    time_required = models.IntegerField()
    instructions = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
