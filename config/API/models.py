from djongo import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Category(models.Model):
    IMPORTANCE_LEVEL_CHOICES = [
        ('M', 'Must'),
        ('S', 'Should'),
        ('C', 'Could'),
        ('W', 'Would'),
        ('N', 'None')
    ]
    name = models.CharField(max_length=128)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # TODO: przetestować czy to w dobrą stronę usuwanie
    description = models.CharField(max_length=256, blank=True)
    # TODO: jak to przechowujemy?
    color = models.CharField(max_length=128, blank=True)
    # TODO: jak to przechowujemy?
    icon = models.CharField(max_length=128, blank=True)
    importance_level = models.CharField(
        max_length=1, choices=IMPORTANCE_LEVEL_CHOICES, default='N')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Activity(models.Model):
    name = models.CharField(max_length=128)
    # TODO: przetestować czy to w dobrą stronę usuwanie
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # TODO: przetestować czy to w dobrą stronę usuwanie
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=256, blank=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    # TODO: add default to date_end - date_start in clean or save
    length = models.DurationField(null=True)
    # TODO: if date_start and date_end is not null then is_planned = True
    is_planned = models.BooleanField(default=False)
    # TODO: add default value to self.category.importance_level to clean or save
    importance_level = models.CharField(
        max_length=1, choices=Category.IMPORTANCE_LEVEL_CHOICES, default='N')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
