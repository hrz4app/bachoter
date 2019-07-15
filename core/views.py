from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.utils.html import escape

from el_pagination.decorators import page_template

from social.views import timeline
from authentication.models import Profile, Buddies
from social.models import Bachot

from .forms import UserEditForm, ProfileForm, ProfilePictureForm

# Create your views here.
def landing(request):
    if request.user.is_authenticated():
        return timeline(request)
    else:
        return render(request, 'core/landing.html')

@page_template('social/__paginate_bachot.html')
@login_required
def profile(request, username, template='core/profile.html', extra_context=None):
    user = request.user
    user_on_page = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    profile_picture_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=profile)
    pending_list = Buddies.get_pending_list(user)
    my_pending_list = Buddies.get_request_list(user)
    buddies_list = Buddies.get_buddies_list(user)
    bachots = Bachot.objects.filter(user=user_on_page).order_by('-timestamp')
    if profile_picture_form.is_valid():
        profile_picture_form.save()
        messages.add_message(request, messages.SUCCESS, "Your profile picture was successfully changed.")
    context = {
        'user_on_page': user_on_page,
        'profile_picture_form': profile_picture_form,
        'pending_list': pending_list,
        'my_pending_list': my_pending_list,
        'buddies_list': buddies_list,
        'bachots': bachots,
        'csrf': str(csrf(request)['csrf_token'])
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@page_template('social/__paginate_buddies.html')
@login_required
def profile_buddies(request, username, template='social/buddies.html', extra_context=None):
    user_on_page = get_object_or_404(User, username=username)
    context = {
        'buddies': Buddies.get_buddies_list(user_on_page),
        'page_header': u"<a href='/{0}/'>{1}</a>'s Buddies.".format(user_on_page.username, user_on_page.profile.get_screen_name()),
        'empty': "{0} have no Buddies.".format(user_on_page.profile.get_screen_name())
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@login_required
def settings_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_form = ProfileForm(request.POST or None, instance=profile)
    if profile_form.is_valid():
        profile_form.save()
        messages.add_message(request, messages.SUCCESS, "Your profile was successfully edited.")
    return render(request, 'core/settings_profile.html', {
        'profile_form': profile_form
    })

@login_required
def settings_accounts(request):
    user = request.user
    user_form = UserEditForm(request.POST or None, instance=user, request=request)
    if user_form.is_valid():
        user_form.save()
        messages.add_message(request, messages.SUCCESS, "Your accounts was successfully edited.")
    return render(request, 'core/settings_accounts.html', {
        'user_form': user_form
    })