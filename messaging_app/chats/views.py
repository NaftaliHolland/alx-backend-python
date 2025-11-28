from django.http import response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation_id"]

    def list(self, request):
        queryset = Conversation.objects.all()
        serializer = ConversationSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        conversation = get_object_or_404(Conversation, pk=pk)

        serializer = ConversationSerializer(conversation)

        return Response(serializer.data)

    def create(self, request):
        serializer = ConversationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ViewSet):
    """
    A viewset for listing messages
    """

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["message_id", "sender_id", "message_body"]

    def list(self, request, converstaion_pk=None):
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
