from djongo import models

class Category(models.Model):
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=128)

class Location(models.Model):
    name = models.CharField(max_length=128)
    coordinates = models.CharField(max_length=256)

class UserData(models.Model):
    user_name = models.CharField(max_length=256)
    e_mail = models.CharField(max_length=512)

