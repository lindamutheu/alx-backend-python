from django.contrib.auth.models import User
from messaging.models import Message, Notification

sender = User.objects.get(username='alice')
receiver = User.objects.get(username='bob')

message = Message.objects.create(sender=sender, receiver=receiver, content="Hey Bob!")

# Check if notification was created
Notification.objects.filter(user=receiver, message=message).exists()
