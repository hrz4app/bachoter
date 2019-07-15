from django.contrib import admin

from .models import Singer, Label, Album, Track

# Register your models here.
admin.site.register(Singer)
admin.site.register(Label)
admin.site.register(Album)
admin.site.register(Track)