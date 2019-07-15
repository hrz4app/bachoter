# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(max_length=1, choices=[('L', 'Liked'), ('D', 'Disliked'), ('C', 'Commented'), ('S', 'Also Commented'), ('A', 'Accepted Request')])),
                ('is_read', models.BooleanField(default=False)),
                ('bachot', models.ForeignKey(to='social.Bachot', blank=True, null=True)),
                ('from_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
