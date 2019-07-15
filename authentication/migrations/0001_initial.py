# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import authentication.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buddies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Buddying')])),
            ],
        ),
        migrations.CreateModel(
            name='Buddy',
            fields=[
                ('code', models.CharField(max_length=12, editable=False, serialize=False, primary_key=True, unique=True, default=authentication.models.Buddy.create_buddy_code)),
                ('tmp_green_reward', models.IntegerField(default=0)),
                ('tmp_red_reward', models.IntegerField(default=0)),
                ('buddies', models.ManyToManyField(to='authentication.Buddy', related_name='_buddy_buddies_+', through='authentication.Buddies')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=25, blank=True, null=True)),
                ('facebook', models.CharField(max_length=50, help_text='Your facebook username.', blank=True, null=True)),
                ('twitter', models.CharField(max_length=50, help_text='Your twitter username.', blank=True, null=True)),
                ('instagram', models.CharField(max_length=50, help_text='Your instagram username.', blank=True, null=True)),
                ('bio', models.TextField(max_length=255, help_text='Sort description of yourself.', blank=True, null=True)),
                ('picture', models.ImageField(upload_to=authentication.models.PathAndRename('profile_pictures/'), default='profile_pictures/default_picture.png')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='buddies',
            name='buddy_object',
            field=models.ForeignKey(related_name='+', to='authentication.Buddy'),
        ),
        migrations.AddField(
            model_name='buddies',
            name='buddy_subject',
            field=models.ForeignKey(related_name='+', to='authentication.Buddy'),
        ),
    ]
