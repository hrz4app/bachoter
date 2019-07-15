from django.template import Library

from authentication.models import Buddies

from messenger.models import Message
from notifications.models import Notification

register = Library()

@register.simple_tag(takes_context=True)
def request_list_count(context):
    user = context['user']
    request_list = Buddies.get_request_list(user)
    return len(request_list)

@register.simple_tag(takes_context=True)
def inbox_count(context):
    user = context['user']
    count = Message.objects.filter(user=user, is_read=False).count()
    return count

@register.simple_tag(takes_context=True)
def likes_percentage(context):
    bachot = context['bachot']
    likes = bachot.likers.count()
    dislikes = bachot.dislikers.count()
    total_votes = likes + dislikes
    try:
        percentage = float(likes)/float(total_votes) * 100
    except ZeroDivisionError:
        percentage = 0
    return percentage

@register.simple_tag(takes_context=True)
def dislikes_percentage(context):
    bachot = context['bachot']
    likes = bachot.likers.count()
    dislikes = bachot.dislikers.count()
    total_votes = likes + dislikes
    try:
        percentage = float(dislikes)/float(total_votes) * 100
    except ZeroDivisionError:
        percentage = 0
    return percentage

@register.simple_tag(takes_context=True)
def notifications_count(context):
    user = context['user']
    count = Notification.objects.filter(to_user=user, is_read=False).count()
    return count