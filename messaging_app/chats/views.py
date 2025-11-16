from django.http import response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status

from .models import Conversation, Message
from .serializers import (ConversationSerializer, MessageSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ViewSet):
    """
    User ViewSet
    """
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConversationViewSet(viewsets.ViewSet):
    """
    A viewset for listing conversations
    """
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Conversation.objects.all()
        serializer = ConversationSerializer(queryset, many=True)

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

    def list(self, request):
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def create(self, request):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

