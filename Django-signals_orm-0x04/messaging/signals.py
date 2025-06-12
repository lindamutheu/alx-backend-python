#week 6 
#signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.db.models.signals import pre_save
from .models import Message, MessageHistory
from django.utils.timezone import now
from django.db.models.signals import post_delete




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
        instance.edited_at = now()



@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Clean up messages (both sent and received)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Clean up notifications
    Notification.objects.filter(user=instance).delete()

    # Clean up message history where user was editor
    MessageHistory.objects.filter(edited_by=instance).delete()