from django.db import models

from django.contrib.auth.models import User
from django.utils.html import escape

from social.models import Bachot

# Create your models here.
class Notification(models.Model):
    LIKED = 'L'
    DISLIKED = 'D'
    COMMENTED = 'C'
    ALSO_COMMENTED = 'S'
    ACCEPTED_REQUEST = 'A'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (DISLIKED, 'Disliked'),
        (COMMENTED, 'Commented'),
        (ALSO_COMMENTED, 'Also Commented'),
        (ACCEPTED_REQUEST, 'Accepted Request')
    )

    _LIKED_TEMPLATE = u'<a href="/{0}/">{1}</a> liked your <a href="/bachot/{2}/">Bachot</a>.'
    _DISLIKED_TEMPLATE = u'<a href="/{0}/">{1}</a> disliked your <a href="/bachot/{2}/">Bachot</a>.'
    _COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> commented on your <a href="/bachot/{2}/">Bachot</a>.'
    _ALSO_COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> also commentend on the <a href="/bachot/{2}/">Bachot</a>.'
    _ACCEPTED_REQUEST_TEMPLATE = u'<a href="/{0}/">{1}</a> accepted your buddy request.'

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)
    bachot = models.ForeignKey(Bachot, null=True, blank=True)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.bachot.pk
            )
        elif self.notification_type == self.DISLIKED:
            return self._DISLIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.bachot.pk
            )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.bachot.pk
            )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.bachot.pk
            )
        elif self.notification_type == self.ACCEPTED_REQUEST:
            return self._ACCEPTED_REQUEST_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
            )
        else:
            return 'Ooops! Something went wrong.'

    @staticmethod
    def notify_like(user, bachot):
        if user != bachot.user:
            Notification.objects.create(
                from_user=user,
                to_user=bachot.user,
                bachot=bachot,
                notification_type=Notification.LIKED)

    @staticmethod
    def notify_dislike(user, bachot):
        if user != bachot.user:
            Notification.objects.create(
                from_user=user,
                to_user=bachot.user,
                bachot=bachot,
                notification_type=Notification.DISLIKED)

    @staticmethod
    def notify_comment(user, bachot):
        if user != bachot.user:
            Notification.objects.create(
                from_user=user,
                to_user=bachot.user,
                bachot=bachot,
                notification_type=Notification.COMMENTED)

    @staticmethod
    def notify_also_comment(user, bachot):
        comments = bachot.comments.all()
        commenters_id = []
        for comment in comments:
            if comment.user != user and comment.user != bachot.user:
                commenters_id.append(comment.user.pk)
        commenters_id = list(set(commenters_id))
        for user_id in commenters_id:
            Notification.objects.create(
                from_user=user,
                to_user_id=user_id,
                bachot=bachot,
                notification_type=Notification.ALSO_COMMENTED)

    @staticmethod
    def notify_accepted_request(user, to_user):
        if user != to_user:
            Notification.objects.create(
                from_user=user,
                to_user=to_user,
                notification_type=Notification.ACCEPTED_REQUEST)