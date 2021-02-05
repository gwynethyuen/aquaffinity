from django.shortcuts import render
from django.db import models

# list of category choices, global variable so it can be referenced in the form.
CAT_CHOICES = [(1, "Announcements"), (2, "Team Events"), (3, "Academics"), (4, "Swim/Dive"), (5, "Misc")]

# swimmer model stores a swimmer id (id is from swimcloud.com), name, hometown, class year, and list of latest times for each event.
class Swimmer(models.Model):
    swimmer_id = models.CharField(max_length=7)
    name = models.CharField(max_length=50, default="John Doe")
    hometown = models.CharField(max_length=50, default="Troy, NY")
    class_year = models.CharField(max_length=2, default="FR")
    event_list = models.TextField(null=True, default="There are no recent events.")

# post model is used to create a discussion post.
class Post(models.Model):
    title = models.CharField(max_length=60, default="Your Post Title")
    body = models.TextField(default="Your Post Text")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=1000, default="John Doe")
    category = models.CharField(max_length=1, default=5, choices=CAT_CHOICES)

# comment model is used to comment on a post.
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)