# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import entertainment.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('aired_date', models.DateField(blank=True, null=True)),
                ('cover', models.ImageField(upload_to=entertainment.models.PathAndRename('track_album_pictures/'), default='track_album_pictures/default_cover.jpg')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('address', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30, help_text='name of singer or band.')),
                ('description', models.TextField(help_text='description of singer or band.', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('album', models.ForeignKey(to='entertainment.Album', blank=True, null=True)),
                ('label', models.ForeignKey(to='entertainment.Label', blank=True, null=True)),
                ('singer', models.ForeignKey(to='entertainment.Singer')),
            ],
        ),
    ]
