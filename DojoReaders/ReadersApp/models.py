from django.db import models

# Create your models here.

class UserManager(models.Manager):
    pass

class BookManager(models.Manager):
    pass

class AuthorManager(models.Manager):
    pass

class User(models.Model):
    name   = models.CharField(max_length = 255)
    alias  = models.CharField(max_length = 255)
    email  = models.CharField(max_length = 255)
    passwd = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Book(models.Model):
    title  = models.CharField(max_length = 255)
    author = models.ForeignKey('Author', related_name="books", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Author(models.Model):
    name   = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    desc = models.TextField()
    rate = models.IntegerField()
    user = models.ForeignKey('User', related_name="reviews", on_delete = models.CASCADE)
    book = models.ForeignKey('Book', related_name="reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
