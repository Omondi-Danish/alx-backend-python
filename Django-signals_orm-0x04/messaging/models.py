from django.conf import settings
from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return (
            self.filter(receiver=user, read=False)
                .only('id', 'sender', 'content', 'timestamp')
        )

class MessageQuerySet(models.QuerySet):
    def with_threads(self):
        return (
            self.select_related('sender', 'receiver', 'parent_message')
                .prefetch_related('replies')
        )

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # Track read/unread status
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    objects = MessageQuerySet.as_manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        status = " (edited)" if self.edited else ""
        return f"Message {self.id} from {self.sender} to {self.receiver}{status}"

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        state = "Read" if self.is_read else "Unread"
        return f"Notification for {self.user} ({state})"

class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"
