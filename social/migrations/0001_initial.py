# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import imagekit.models.fields
import location_field.models.plain
import social.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BachListening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('caption', models.TextField(max_length=255)),
                ('track_title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BachLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('caption', models.TextField(max_length=255)),
                ('picture', imagekit.models.fields.ProcessedImageField(upload_to=social.models.PathAndRename('bachot_pictures/'), blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, help_text='click the place in map to set point')),
            ],
        ),
        migrations.CreateModel(
            name='Bachot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bachot_type', models.CharField(max_length=1, choices=[('T', 'Text'), ('P', 'Picture'), ('L', 'Location'), ('R', 'Reading to'), ('N', 'Listening to'), ('W', 'Watching')])),
                ('dislikers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='disliking')),
                ('likers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='liking')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BachotComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(max_length=255)),
                ('bachot', models.ForeignKey(related_name='comments', to='social.Bachot')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BachPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('caption', models.TextField(max_length=255)),
                ('picture', imagekit.models.fields.ProcessedImageField(upload_to=social.models.PathAndRename('bachot_pictures/'))),
                ('bachot', models.OneToOneField(to='social.Bachot')),
            ],
        ),
        migrations.CreateModel(
            name='BachText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField(max_length=255)),
                ('bachot', models.OneToOneField(to='social.Bachot')),
            ],
        ),
        migrations.AddField(
            model_name='bachlocation',
            name='bachot',
            field=models.OneToOneField(to='social.Bachot'),
        ),
        migrations.AddField(
            model_name='bachlistening',
            name='bachot',
            field=models.OneToOneField(to='social.Bachot'),
        ),
    ]
