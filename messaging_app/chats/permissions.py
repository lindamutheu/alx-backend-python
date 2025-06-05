#week 5 assignment task 0

from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Object can be a Message or Conversation
        user = request.user

        if isinstance(obj, Message):
            return user in obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            return user in obj.participants.all()
        
        return False
