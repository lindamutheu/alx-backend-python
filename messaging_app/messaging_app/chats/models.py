import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class users (models.Model):
         class Role(models.TextChoices):
          GUEST = 'guest', 'Guest'
         HOST = 'host', 'Host'
         ADMIN = 'admin', 'Admin'

         user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
         first_name = models.CharField(max_length=255)
         last_name = models.CharField(max_length=255)
         email = models.EmailField(unique=True)
         password_hash = models.CharField(max_length=255)
         phone_number = models.CharField(max_length=20, null=True, blank=True)
         role = models.CharField(max_length=10, choices=Role.choices)
         created_at = models.DateTimeField(auto_now_add=True)
    
         def __str__(self):
      
            return f"{self.user_id} {self.email} {self.password_hash} {self.phone_number} {self.role} {self.created_at}{self.first_name} {self.last_name}"


# Conversations model

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(users, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Conversation {self.conversation_id}"
    
    #Mesage model
    
    
    class Message(models.Model):
     message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
     message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(users, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(users, on_delete=models.CASCADE, related_name='received_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"From {self.sender} to {self.recipient} at {self.sent_at}"