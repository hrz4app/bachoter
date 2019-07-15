import os
import bleach
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.html import escape

from location_field.models.plain import PlainLocationField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from entertainment.models import Track

# Create your models here.
@deconstructible
class PathAndRename(object):

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        now = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        ext = filename.split('.')[-1]
        filename = '{}_{}.{}'.format(instance.bachot.id, now, ext)
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename('bachot_pictures/')

class Bachot(models.Model):
    TEXT = 'T'
    PICTURE = 'P'
    LOCATION = 'L'
    READING = 'R'
    LISTENING = 'N'
    WATCHING = 'W'

    BACHOT_TYPES = (
        (TEXT, 'Text'),
        (PICTURE, 'Picture'),
        (LOCATION, 'Location'),
        (READING, 'Reading to'),
        (LISTENING, 'Listening to'),
        (WATCHING, 'Watching'),
    )

    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, related_name='liking')
    dislikers = models.ManyToManyField(User, related_name='disliking')
    bachot_type = models.CharField(max_length=1, choices=BACHOT_TYPES)

class BachText(models.Model):
    bachot = models.OneToOneField(Bachot, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)

    def linkify_text(self):
        return bleach.linkify(escape(self.text))

class BachPicture(models.Model):
    bachot = models.OneToOneField(Bachot, on_delete=models.CASCADE)
    caption = models.TextField(max_length=255)
    picture = ProcessedImageField(upload_to=path_and_rename,
                                  format='JPEG',
                                  options={'quality': 70})


    def linkify_caption(self):
        return bleach.linkify(escape(self.caption))

class BachLocation(models.Model):
    bachot = models.OneToOneField(Bachot, on_delete=models.CASCADE)
    caption = models.TextField(max_length=255)
    picture = ProcessedImageField(upload_to=path_and_rename,
                                  null=True,
                                  blank=True,
                                  format='JPEG',
                                  options={'quality': 70})
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=11, help_text='click the place in map to set point')

    def linkify_caption(self):
        return bleach.linkify(escape(self.caption))

class BachListening(models.Model):
    bachot = models.OneToOneField(Bachot, on_delete=models.CASCADE)
    caption = models.TextField(max_length=255)
    track_title = models.CharField(max_length=50)

    def linkify_caption(self):
        return bleach.linkify(escape(self.caption))

    def get_track(self):
        title, singer = self.track_title.split(' -- ')
        track = Track.objects.get(title=title, singer__name=singer)
        return track

class BachotComments(models.Model):
    bachot = models.ForeignKey(Bachot, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=255)

    def linkify_text(self):
        return bleach.linkify(escape(self.text))