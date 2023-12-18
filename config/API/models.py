from djongo import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass


class Category(models.Model):
    IMPORTANCE_LEVEL_CHOICES = [
        ('M', 'Must'),
        ('S', 'Should'),
        ('C', 'Could'),
        ('W', 'Would'),
        ('N', 'None'),
        ('n', 'None')
    ]
    name = models.CharField(max_length=128)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, blank=True)
    color = models.CharField(max_length=10, blank=True, help_text="hex")
    icon = models.CharField(max_length=128, blank=True)
    importance_level = models.CharField(
        max_length=1, choices=IMPORTANCE_LEVEL_CHOICES, default='n')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Activity(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=256, blank=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    length = models.DurationField(null=True)
    is_planned = models.BooleanField(default=False)
    importance_level = models.CharField(
        max_length=1, choices=Category.IMPORTANCE_LEVEL_CHOICES, default='n')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise ValidationError(
                    'date_start must be less than or equal to date_end')
    
            self.length = self.date_end - self.date_start
            self.is_planned = True
        if self.importance_level == 'n':
            self.importance_level = self.category.importance_level
        super(Activity, self).save(*args, **kwargs)
