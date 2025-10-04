from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if not created:
        return

    # Create a notification entry for the message receiver
    Notification.objects.create(
        user=instance.receiver,
        message=instance
    )
