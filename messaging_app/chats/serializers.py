from rest_framework import serializers

from .models import Conversation, Message, User

# TODO: Add nested serailizer for sender and recepient: Maybe

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'message_body',
            'sent_at',
        ]

class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants_id',
            'messages',
            'created_at',
        ]

    def get_messages(self, obj):
        participants = obj.participants_id.all()
        return MessageSerializer(
            Message.objects.filter(sender_id__in=participants).order_by("sent_at"),
            many=True,
        ).data
