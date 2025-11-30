from chats.models import Conversation
from django.shortcuts import get_object_or_404
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants in a conversation to access the view.
    """

    def has_permission(self, request, view):
        conversation_pk = view.kwargs.get("conversation_pk")

        if not conversation_pk:
            return False 

        try:
            conversation = Conversation.objects.get(pk=conversation_pk)
        except Conversation.DoesNotExist:
            return False

        return conversation.participants_id.filter(pk=request.user.pk).exists()

    def has_object_permission(self, request, view, obj):
        """
        Check if user is part of the conversation
        """
        from chats.models import Conversation

        conversation_pk = view.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, pk=conversation_pk)

        return conversation.participants_id.filter(pk=request.user.pk).exists()
