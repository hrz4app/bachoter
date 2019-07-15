from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf

from el_pagination.decorators import page_template

from authentication.models import Buddies
from authentication.decorators import ajax_required
from entertainment.models import Track
from notifications.models import Notification

from .models import Bachot, BachText, BachPicture, BachLocation, BachListening, BachotComments
from .forms import TextForm, PictureForm, LocationForm, ListeningForm

# Create your views here.
@login_required
@ajax_required
def bachot_form(request):
    script = False
    all_track = None
    if request.GET.get('t'):
        bachot_type = request.GET['t']
        if bachot_type == Bachot.TEXT:
            form = TextForm()
        elif bachot_type == Bachot.PICTURE:
            form = PictureForm()
        elif bachot_type == Bachot.LOCATION:
            form = LocationForm()
        elif bachot_type == Bachot.LISTENING:
            form = ListeningForm()
            script = True
            all_track = []
            tmp_all_track = Track.objects.all()
            for track in tmp_all_track:
                all_track.append("{0} -- {1}".format(track.title, track.singer))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest
    context = {
        'form': form,
        'bachot_type': bachot_type,
        'script': script
    }
    if all_track is not None:
        context.update({'all_track': all_track})
    return render(request, 'social/bachot_form.html', context)

@page_template('social/__paginate_bachot.html')
@login_required
def timeline(request, template='social/timeline.html', extra_context=None):
    user = request.user
    buddies_list = Buddies.get_buddies_list(user)
    bachot_list = Bachot.objects.filter(user=user)
    buddies_bachot_list = Bachot.objects.filter(user__buddy__in=buddies_list)
    bachots = (bachot_list | buddies_bachot_list).order_by('-timestamp')
    context = {
        'bachots': bachots,
        'csrf': str(csrf(request)['csrf_token']),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@page_template('social/__paginate_buddies.html')
@login_required
def buddies(request, template='social/buddies.html', extra_context=None):
    user = request.user
    context = {
        'buddies': Buddies.get_buddies_list(user),
        'page_header': "My Buddies",
        'empty': "You have no Buddies."
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@page_template('social/__paginate_buddies.html')
@login_required
def buddies_request(request, template='social/buddies.html', extra_context=None):
    user = request.user
    context = {
        'buddies': Buddies.get_request_list(user),
        'page_header': "Request Buddies",
        'empty': "You have no Request Buddies."
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@page_template('social/__paginate_buddies.html')
@login_required
def buddies_pending(request, template='social/buddies.html', extra_context=None):
    user = request.user
    context = {
        'buddies': Buddies.get_pending_list(user),
        'page_header': "Pending Buddies",
        'empty': "You have no Pending Buddies."
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@login_required
@ajax_required
def buddy_click(request):
    buddy_subject_id = request.POST.get('buddy_subject_id', None)
    buddy_object_id = request.POST.get('buddy_object_id', None)
    buddy_action = request.POST.get('buddy_action', None)
    if buddy_action == 'buddy':
        Buddies.objects.create(
            buddy_subject_id=buddy_subject_id,
            buddy_object_id=buddy_object_id,
            status=Buddies.PENDING)
        buddying = 'buddy'
    elif buddy_action == 'accept':
        b = Buddies.objects.get(
            buddy_subject_id=buddy_subject_id,
            buddy_object_id=buddy_object_id)
        b.status = Buddies.BUDDYING
        b.save()
        buddying = 'accept'
        Notification.notify_accepted_request(b.buddy_object.user, b.buddy_subject.user)
    elif buddy_action == 'unbuddy' or buddy_action == 'cancel':
        Buddies.objects.get(
            Q(buddy_subject_id=buddy_subject_id,
            buddy_object_id=buddy_object_id) | 
            Q(buddy_subject_id=buddy_object_id,
            buddy_object_id=buddy_subject_id)
            ).delete()
        buddying = 'delete'
    else:
        return HttpResponseBadRequest('Unknown action: {}'.format(buddy_action))
    return HttpResponse(buddying)

@login_required
def bachot(request, pk):
    bachot = get_object_or_404(Bachot, pk=pk)
    buddies_list = Buddies.get_buddies_list(bachot.user)
    return render(request, 'social/bachot.html', {
        'buddies_list': buddies_list,
        'bachot': bachot
    })

@login_required
@ajax_required
def bachot_create(request):
    user = request.user
    bachot_type = request.POST.get('bachot_type', None)
    bachot = Bachot(user=user, bachot_type=bachot_type)
    if bachot_type == Bachot.TEXT:
        bachtext_form = TextForm(request.POST)
        if bachtext_form.is_valid():
            bachot.save()
            text = request.POST.get('text', None)[:255]
            BachText.objects.create(bachot=bachot, text=text)
            return render(request, 'social/_bachot.html', {
                'bachot': bachot,
                'csrf': str(csrf(request)['csrf_token'])
            })
        else:
            return HttpResponseBadRequest('Unknown.')
    elif bachot_type == Bachot.PICTURE:
        bachpicture_form = PictureForm(request.POST, request.FILES)
        if bachpicture_form.is_valid():
            bachot.save()
            caption = request.POST.get('caption', None)[:255]
            picture = request.FILES.get('picture', None)
            bachpicture = BachPicture(bachot=bachot, caption=caption)
            bachpicture.picture.save(picture.name, picture)
            return render(request, 'social/_bachot.html', {
                'bachot': bachot,
                'csrf': str(csrf(request)['csrf_token'])
            })
        else:
            return HttpResponseBadRequest('Unknown.')
    elif bachot_type == Bachot.LOCATION:
        bachlocation_form = LocationForm(request.POST, request.FILES)
        if bachlocation_form.is_valid():
            bachot.save()
            caption = request.POST.get('caption', None)[:255]
            picture = request.FILES.get('picture', None)
            name = request.POST.get('name', None)
            city =  request.POST.get('city', None)
            location =  request.POST.get('location', None)
            if picture:
                bachlocation = BachLocation(bachot=bachot, caption=caption, name=name, city=city, location=location, picture=picture)
                bachlocation.picture.save(picture.name, picture)
            else:
                bachlocation = BachLocation(bachot=bachot, caption=caption, name=name, city=city, location=location)
                bachlocation.save()
            return render(request, 'social/_bachot.html', {
                'bachot': bachot,
                'csrf': str(csrf(request)['csrf_token'])
            })
    elif bachot_type == Bachot.LISTENING:
        bachListening_form = ListeningForm(request.POST)
        if bachListening_form.is_valid():
            bachot.save()
            caption = request.POST.get('caption', None)[:255]
            track_title = request.POST.get('track_title', None)
            bachlistening = BachListening.objects.create(bachot=bachot, caption=caption, track_title=track_title)
            return render(request, 'social/_bachot.html', {
                'bachot': bachot,
                'csrf': str(csrf(request)['csrf_token'])
            })
    else:
        return HttpResponseBadRequest('Unknown')

@login_required
@ajax_required
def bachot_like_or_dislike(request):
    user = request.user
    bachot_id = request.POST.get('bachot_id', None)
    likes_dislikes = request.POST.get('likes_dislikes', None)
    bachot = Bachot.objects.get(pk=bachot_id)
    buddy_bachot = bachot.user.buddy
    if likes_dislikes == 'like':
        bachot.likers.add(user)
        result = "Liked"
        fa = 'up'
        Notification.notify_like(user, bachot)
        if bachot.user != user:
            buddy_bachot.tmp_green_reward = buddy_bachot.tmp_green_reward + 1
            buddy_bachot.save()
    elif likes_dislikes == 'dislike':
        bachot.dislikers.add(user)
        result = "Disliked"
        fa = 'down'
        Notification.notify_dislike(user, bachot)
        if bachot.user != user:
            buddy_bachot.tmp_red_reward = buddy_bachot.tmp_red_reward + 1
            buddy_bachot.save()
    else:
        return HttpResponseBadRequest('Unknown')
    likes = bachot.likers.count()
    dislikes = bachot.dislikers.count()
    total_votes = likes + dislikes
    try:
        likes_percentage = float(likes)/float(total_votes) * 100
    except ZeroDivisionError:
        likes_percentage = 0
    try:
        dislikes_percentage = float(dislikes)/float(total_votes) * 100
    except ZeroDivisionError:
        dislikes_percentage = 0
    return render(request, 'social/_like_replacer.html', {
        'bachot': bachot,
        'result': result,
        'likes_percentage': likes_percentage,
        'dislikes_percentage': dislikes_percentage,
        'fa': fa
    })

@login_required
@ajax_required
def bachot_delete(request):
    user = request.user
    bachot_id = request.POST.get('bachot_id', None)
    bachot = Bachot.objects.get(pk=bachot_id)
    if bachot.user == user:
        bachot.delete()
    else:
        return HttpResponseForbidden()
    return HttpResponse()

@login_required
@ajax_required
def get_bachot_comments(request):
    if request.GET.get('b'):
        bachot_id = request.GET['b']
        bachot = Bachot.objects.get(pk=bachot_id)
        comments = bachot.comments.all()
        return render(request, 'social/comments_in_modal.html', {
            'comments': comments,
            'csrf': str(csrf(request)['csrf_token'])
        })
    else:
        return HttpResponseBadRequest('Unknown')

@login_required
@ajax_required
def bachot_comment(request):
    user = request.user
    bachot_id = request.POST.get('bachot_id', None)
    bachot = Bachot.objects.get(pk=bachot_id)
    text = request.POST.get('text', None)[:255]
    new_comment = BachotComments(bachot=bachot, user=user, text=text)
    new_comment.save()
    Notification.notify_comment(user, bachot)
    Notification.notify_also_comment(user, bachot)
    return render(request, 'social/_comments_in_modal.html', {
        'comment': new_comment,
        'csrf': str(csrf(request)['csrf_token'])
    })

@login_required
@ajax_required
def bachot_comment_delete(request):
    user = request.user
    comment_id = request.POST.get('comment_id', None)
    comment = BachotComments.objects.get(pk=comment_id)
    if comment.user == user:
        comment.delete()
    else:
        return HttpResponseForbidden()
    count = comment.bachot.comments.count()
    return HttpResponse(count)