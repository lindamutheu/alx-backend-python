#week 5 assignment task 0

from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access or modify its messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Safe methods like GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return self._is_participant(obj, user)

        # For PUT, PATCH, DELETE — also check if user is participant
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return self._is_participant(obj, user)

        # For POST or others
        return self._is_participant(obj, user)

    def _is_participant(self, obj, user):
        if isinstance(obj, Conversation):
            return user in obj.participants.all()
        if isinstance(obj, Message):
            return user in obj.conversation.participants.all()
        return False