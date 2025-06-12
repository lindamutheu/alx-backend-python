#week 6 
#signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.db.models.signals import pre_save
from .models import Message, MessageHistory




@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message; nothing to compare

    try:
        original = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content has changed
    if instance.content != original.content:
        # Save previous content to history
        MessageHistory.objects.create(
            message=original,
            old_content=original.content
        )
        # Mark message as edited
        instance.edited = True