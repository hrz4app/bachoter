import os
from datetime import datetime
from uuid import uuid4

from django.db import models
from django.utils.deconstruct import deconstructible

# Create your models here.
@deconstructible
class PathAndRename(object):

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        now = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        ext = filename.split('.')[-1]
        filename = '{}_{}.{}'.format(instance.name, now, ext)
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename('track_album_pictures/')

class Singer(models.Model):
    name = models.CharField(max_length=30, help_text='name of singer or band.')
    description = models.TextField(null=True, blank=True, help_text='description of singer or band.')

    def __str__(self):
        return self.name

class Label(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=50)
    aired_date = models.DateField(blank=True, null=True)
    cover = models.ImageField(upload_to=path_and_rename, default='track_album_pictures/default_cover.jpg')

    def __str__(self):
        return self.name

class Track(models.Model):
    singer = models.ForeignKey(Singer)
    label = models.ForeignKey(Label, null=True, blank=True)
    album = models.ForeignKey(Album, null=True, blank=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title