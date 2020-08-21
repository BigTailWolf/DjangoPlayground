from django.db import models
# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['user_name']) < 2:
            errors['user_name'] = 'Name should be at least 2 characters'
        if len(postData['user_alias']) < 2:
            errors['user_alias'] = 'Alias should be at least 2 characters'

        user_email = postData['user_email']
        if len(user_email) < 5:
            errors['user_email'] = 'Email should be at least 5 characters'
        if len(self.filter(email=user_email)) > 0:
            errors['email_dedupe'] = 'Email is already registered here'

        user_passwd = postData['user_passwd']
        if len(user_passwd) < 8:
            errors['user_password'] = 'Password has to be at least 8 characters'
        
        if user_passwd != postData['user_passwd_repeat']:
            errors['user_pw_confirm'] = 'Your confirm does not match'

        return errors


class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        book_title = postData['book_title']

        if len(book_title) < 3:
            errors['book_title'] = 'Title should be at least 3 characters'
        if len(self.filter(title=book_title)) > 0:
            errors['book_dedupe'] = 'Book already added'
        
        return errors


class AuthorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print(postData)
        if postData['author_selection'] == '0':
            author_name = postData['author_name']
            if len(author_name) < 5:
                errors['author_name'] = 'Author name should be at least 5 characters'
            if len(self.filter(name=author_name)) > 0:
                errors['author_name'] = 'Author already exists'
        
        print(errors)
        return errors


class User(models.Model):
    name   = models.CharField(max_length = 255)
    alias  = models.CharField(max_length = 255)
    email  = models.CharField(max_length = 255)
    passwd = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Book(models.Model):
    title  = models.CharField(max_length = 255)
    author = models.ForeignKey('Author', related_name="books", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class Author(models.Model):
    name   = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AuthorManager()

class Review(models.Model):
    desc = models.TextField()
    rate = models.IntegerField()
    user = models.ForeignKey('User', related_name="reviews", on_delete = models.CASCADE)
    book = models.ForeignKey('Book', related_name="reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
