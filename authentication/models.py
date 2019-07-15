import os
from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.utils.deconstruct import deconstructible

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
@deconstructible
class PathAndRename(object):

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        now = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        ext = filename.split('.')[-1]
        filename = '{}_{}.{}'.format(instance.user.username, now, ext)
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename('profile_pictures/')

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=25, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True, help_text='Your facebook username.')
    twitter = models.CharField(max_length=50, null=True, blank=True, help_text='Your twitter username.')
    instagram = models.CharField(max_length=50, null=True, blank=True, help_text='Your instagram username.')
    bio = models.TextField(max_length=255, null=True, blank=True, help_text='Sort description of yourself.')
    picture = models.ImageField(upload_to=path_and_rename, default='profile_pictures/default_picture.png')
    picture_thumbnail = ImageSpecField(source='picture',
                                       processors=[ResizeToFill(100, 100)],
                                       format='JPEG',
                                       options={'quality': 100})

    def get_screen_name(self):
        try:
            if self.name:
                return self.name
            else:
                return self.user.username
        except:
            return self.user.username

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class Buddy(models.Model):
    def create_buddy_code():
        return "BCo" + uuid4().hex[:9].upper()

    code = models.CharField(max_length=12, primary_key=True, unique=True, editable=False, default=create_buddy_code)
    user = models.OneToOneField(User)
    buddies = models.ManyToManyField('self', through='Buddies', related_name='+', symmetrical=False)
    tmp_green_reward = models.IntegerField(default=0)
    tmp_red_reward = models.IntegerField(default=0)

    @property
    def green_reward(self):
        return int(self.tmp_green_reward / 3)

    @property
    def red_reward(self):
        return int(self.tmp_red_reward / 5)

    @property
    def total_point(self):
        total=int(self.green_reward - self.red_reward)
        if total < 0:
            return 0
        else:
            return total

def create_user_buddy(sender, instance, created, **kwargs):
  if created:
      Buddy.objects.create(user=instance)

def save_user_buddy(sender, instance, **kwargs):
  instance.buddy.save()

post_save.connect(create_user_buddy, sender=User)
post_save.connect(save_user_buddy, sender=User)

class BuddiesManager(models.Manager):
    def pending(self):
        return self.filter(status=Buddies.PENDING)

    def buddies(self):
        return self.filter(status=Buddies.BUDDYING)

class Buddies(models.Model):
    PENDING = 0
    BUDDYING = 1

    BUDDY_STATUSES = (
        (PENDING, 'Pending'),
        (BUDDYING, 'Buddying'),
    )

    buddy_subject = models.ForeignKey(Buddy, related_name='+')
    buddy_object = models.ForeignKey(Buddy, related_name='+')
    status = models.IntegerField(choices=BUDDY_STATUSES)
    objects = BuddiesManager()

    @staticmethod
    def get_buddies_list(user):
        temp_buddies_list = Buddies.objects.buddies().filter(Q(buddy_object=user.buddy) | Q(buddy_subject=user.buddy)).order_by('-pk')
        buddies_list = []
        for buddies in temp_buddies_list:
            if user.buddy == buddies.buddy_subject:
                buddies_list.append(buddies.buddy_object.user.buddy)
            else:
                buddies_list.append(buddies.buddy_subject.user.buddy)
        return buddies_list

    @staticmethod
    def get_request_list(user):
        temp_pending_list = Buddies.objects.pending().filter(buddy_object=user.buddy).order_by('-pk')
        pending_list = []
        for buddies in temp_pending_list:
            pending_list.append(buddies.buddy_subject.user.buddy)
        return pending_list

    @staticmethod
    def get_pending_list(user):
        temp_pending_list = Buddies.objects.pending().filter(buddy_subject=user.buddy).order_by('-pk')
        pending_list = []
        for buddies in temp_pending_list:
            pending_list.append(buddies.buddy_object.user.buddy)
        return pending_list