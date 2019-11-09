from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Notice(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=50)
    date_posted =  models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=30,default=0)
    verify=models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Post(models.Model):
    title  = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Book(models.Model):
    bookid =models.CharField(primary_key=True, max_length=20,default=0)
    title = models.CharField(max_length=200)
    content = models.TextField()
    quantity = models.IntegerField(max_length=10)
    author = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    count = models.IntegerField(max_length=5, default=0)
    rcount = models.IntegerField(max_length=5, default=0)
    ecount = models.IntegerField(max_length=5, default=0)
    pcount = models.IntegerField(max_length=5, default=0)

    def __str__(self):
        return self.username

class IssueBook(models.Model):
    bookid = models.CharField(primary_key=True,max_length=50,default=0)
    user =models.CharField(max_length=50)
    title =models.CharField(max_length=30)
    author =models.CharField(max_length=30)
    subject =models.CharField(max_length=20)
    issuedate = models.DateTimeField(default=timezone.now)

    def __str__(self):
       return self.user
