from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets, filters
from .models import Conversation, Message
from rest_framework.response import Response #week 5
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated #week 5
from .permissions import IsParticipantOfConversation #week 5
from django_filters.rest_framework import DjangoFilterBackend #week 5
from .filters import MessageFilter #week 5


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['participants__username']  
    ordering_fields = ['created_at']

    serializer_class = ConversationSerializer #week 5 assignment
    permission_classes = [IsAuthenticated, IsParticipantOfConversation] #week five

    
    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user not in instance.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()







class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  #week five assgnment
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user not in instance.conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
