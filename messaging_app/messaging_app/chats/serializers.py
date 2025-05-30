# hats/serializers.py

from rest_framework import serializers
from .models import CustomUser, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'recipient', 'message_body', 'sent_at']


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        # Get all messages where conversation is this one
        messages = Message.objects.filter(conversation=obj).order_by('sent_at')
        return MessageSerializer(messages, many=True).data
