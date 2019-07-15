from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from authentication.models import Profile

# Create your views here.
@login_required
def search(request):
    if 'buddy' in request.GET:
        q = request.GET.get('buddy')
        if len(q) == 0:
            return redirect('/search/')
        results = User.objects.filter(username__icontains=q)
        count = results.count()
        return render(request, 'search/results.html', {
            'q': q,
            'count': count,
            'results': results,
        })
    else:
        return render(request, 'search/search.html', {
        	'hide_search': True
        })