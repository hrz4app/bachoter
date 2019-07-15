from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Track

# Create your views here.
@login_required
def music_track(request, pk):
    music_track = get_object_or_404(Track, id=pk)
    return render(request, 'entertainment/music_track.html', {
        'track': music_track
    })