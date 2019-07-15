from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, related_name='+')
    message = models.TextField(max_length=1000, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+')
    from_user = models.ForeignKey(User, related_name='+')
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('timestamp',)
        db_table = 'messages_message'

    def __str__(self):
        return self.message

    @staticmethod
    def send_message(from_user, to_user, message):
        message = message[:1000]
        current_user_message = Message(from_user=from_user,
            message=message,
            user=from_user,
            conversation=to_user,
            is_read=True)
        current_user_message.save()
        Message(from_user=from_user,
            conversation=from_user,
            message=message,
            user=to_user).save()
        return current_user_message

    @staticmethod
    def get_conversations(user):
        '''
            select "messages_message"."conversation_id",
            max("messages_message"."timestamp") as "last"
            from "messages_message"
            where "messages_message"."user_id" = 4
            group by "messages_message"."conversation_id"
            order by "last" desc
        '''
        '''[
            {'last': datetime.xxx, 'conversation': 2},
            {'last': datetime.xxx, 'conversation': 3}
        ]'''
        conversations = Message.objects.filter(user=user).values('conversation').annotate(last=Max('timestamp')).order_by('-last')
        users = []
        for conversation in conversations:
            users.append({
                'user': User.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                'unread': Message.objects.filter(user=user, conversation__pk=conversation['conversation'], is_read=False).count(),
            })
        '''user = [{'user': user, 'last': datetime.xxx, 'unread': 0}]'''
        return users