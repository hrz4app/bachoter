from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from el_pagination.decorators import page_template

from authentication.decorators import ajax_required

from .models import Message

# Create your views here.
@login_required
def default_messages(request):
    conversations = Message.get_conversations(user=request.user)
    return render(request, 'messenger/default_messages.html', {
        'conversations': conversations
    })

@login_required
def new_messages(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        try:
            to_user = User.objects.get(username=to_user_username)
        except Exception:
            return redirect('/messages/')
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return redirect('/messages/new/')
        if from_user != to_user:
            Message.send_message(from_user, to_user, message)
        return redirect(u'/messages/{0}/'.format(to_user_username))
    else:
        u = ""
        if 'u' in request.GET:
            u = request.GET['u']
        conversations = Message.get_conversations(user=request.user)
        return render(request, 'messenger/new_messages.html', {
            'conversations': conversations,
            'u': u
        })

@page_template('messenger/__paginate_with_message.html')
@login_required
def with_messages(request, username, template='messenger/with_messages.html', extra_context=None):
    conversations = Message.get_conversations(user=request.user)
    active_conversation = username
    messages = Message.objects.filter(user=request.user, conversation__username=username).order_by('-timestamp')
    messages.update(is_read=True)
    for conversation in conversations:
        if conversation['user'].username == username:
            conversation['unread'] = 0
    context = {
        'messages': messages,
        'conversations': conversations,
        'active': active_conversation
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

@login_required
@ajax_required
def send_messages(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return HttpResponse()
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message)
            return render(request, 'messenger/_with_messages_list.html', {'message': msg})
        return HttpResponse()
    else:
        return HttpResponseBadRequest()