from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Channel, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_moderator']

class ChannelSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'users']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    channel = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'channel', 'text', 'timestamp']
