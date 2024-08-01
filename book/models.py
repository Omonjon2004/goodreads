import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.

class Users(AbstractUser):
    middle_name = models.CharField(max_length=56, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    login_try_count=models.IntegerField(default=0)

class Book(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=128)
    published = models.DateField()
    isbn = models.CharField(max_length=128, unique=True)
    language = models.CharField(max_length=12, blank=True, null=True)
    page = models.IntegerField()
    authors = models.ManyToManyField("Author",related_name="authors")
    genre=models.ManyToManyField('Genre', related_name='book_genre')
    picture = models.ImageField(upload_to="book/", null=True, blank=True)
    # owner_id=models.ManyToManyField("Users",related_name="owner")

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    birthday = models.DateField()
    website = models.URLField(blank=True)
    about = models.TextField()
    avatar = models.ImageField(upload_to="avatar/")
    genre=models.ForeignKey('Genre', models.SET_NULL, null=True, blank=True,related_name='author_genre')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Bookshelf(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(Users, models.CASCADE, "user_shelf")
    books = models.ManyToManyField(Book, "books_shelf")

class BookReview(models.Model):
    body = models.TextField()
    book = models.ForeignKey(Book, models.CASCADE, "reviws")
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    owner = models.ForeignKey(Users, models.CASCADE, "reviews")
    like_count = models.IntegerField(default=0)


class BlockedUsers(models.Model):
    username = models.CharField(max_length=150)


    def __str__(self):
        return self.username