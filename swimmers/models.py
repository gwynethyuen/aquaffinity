from django.db import models

class Swimmer(models.Model):
	first = models.CharField(max_length=20)
	last = models.CharField(max_length=20)
	image = models.FilePathField(path='/static/img')


    # title = models.CharField(max_length=100)
    # description = models.TextField()
    # technology = models.CharField(max_length=20)
    # image = models.FilePathField(path="/img")