from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # ✅ "conversation_id" explicitly used from query params
        conversation_id = self.request.query_params.get("conversation_id")

        # ✅ Message.objects.filter used for queryset
        if conversation_id:
            return Message.objects.filter(
                conversation__id=conversation_id,
                conversation__participants=self.request.user
            )
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)