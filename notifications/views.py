from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from el_pagination.decorators import page_template

from .models import Notification

# Create your views here.
@page_template('notifications/__paginate_notifications.html')
@login_required
def notifications(request, template='notifications/notifications.html', extra_context=None):
    user = request.user
    notifications = Notification.objects.filter(to_user=user).order_by('-timestamp')
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()
    context = {
        'notifications': notifications
    }
    if extra_context is not None:
        context.update(extra_context) 
    return render(request, template, context)