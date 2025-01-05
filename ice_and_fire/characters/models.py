from django.db import models

from users.models import CustomUser


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    cover = models.ImageField(upload_to='media/covers/', blank=True, null=True)
    is_ice_and_fire = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class House(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    url = models.URLField(max_length=256, blank=True, null=True)
    coat = models.URLField(max_length=256, blank=True, null=True)
    words = models.CharField(max_length=100, blank=True, null=True)
    lord = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    founder = models.CharField(max_length=100, blank=True, null=True)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    url = models.URLField(max_length=256, blank=True, null=True)
    photo = models.URLField(max_length=256, blank=True, null=True)
    books = models.ManyToManyField(Book)
    # house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserBook(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
