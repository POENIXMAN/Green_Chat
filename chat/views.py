from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Channel, Message
from .serializers import UserSerializer, ChannelSerializer, MessageSerializer

User = get_user_model()

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=request.data['password']
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PromoteToModeratorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:  
            return Response({'error': 'Permission denied'}, status=403)
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            user.is_moderator = True
            user.save()
            return Response({'message': f'User {user.username} is now a moderator'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class ChannelListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        channels = Channel.objects.all()
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_moderator:
            return Response({'error': 'Only moderators can create channels'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        channel_id = request.query_params.get('channel_id')
        if not channel_id:
            return Response({'error': 'channel_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user is part of the channel
        if not request.user.channels.filter(id=channel_id).exists():
            return Response({'error': 'You are not a member of this channel'}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(channel_id=channel_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the logged-in user as the sender
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Block User by Moderator
class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_moderator:
            return Response({'error': 'Only moderators can block users'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_to_block = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user_to_block.is_active = False
        user_to_block.save()
        return Response({'message': f'User {user_to_block.username} has been blocked'}, status=status.HTTP_200_OK)
