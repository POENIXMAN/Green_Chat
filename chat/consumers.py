import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer

# Set up logging
logger = logging.getLogger(__name__)



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            import jwt
            from asgiref.sync import sync_to_async
            # Extract token from query string or headers
            logger.debug("Connection attempt started.")
            token = self.scope['query_string'].decode('utf-8').split('=')[-1]
            decoded_payload = jwt.decode(token, options={"verify_signature": False})
            logger.debug(f"Token received: {decoded_payload}")
            
            # Extract user ID from the payload
            user_id = decoded_payload.get('user_id')
            if not user_id:
                logger.error("Token is missing user_id.")
                await self.close(code=403)
                return

            # Validate the token
            from rest_framework_simplejwt.tokens import UntypedToken
            from django.contrib.auth.models import AnonymousUser
            from .models import User, Channel

            try:
                # Verify token validity
                UntypedToken(token)
                
                # Fetch the user based on user_id from the token
                user = await sync_to_async(User.objects.get)(id=user_id)
                self.scope['user'] = user
                logger.debug(f"User authenticated: {user.username}")
            except User.DoesNotExist:
                logger.error(f"User with ID {user_id} does not exist.")
                await self.close(code=403)
                return
            except Exception as e:
                logger.error(f"Authentication failed: {str(e)}")
                self.scope['user'] = AnonymousUser()
                await self.close(code=403)
                return

            # Ensure the user is authenticated
            if not self.scope['user'].is_authenticated:
                logger.error("User is not authenticated.")
                await self.close(code=403)
                return

            # Verify user access to the channel
            self.channel_id = self.scope['url_route']['kwargs']['channel_id']
            logger.debug(f"Channel ID: {self.channel_id}")
            try:
                channel_exists = await sync_to_async(Channel.objects.filter(id=self.channel_id).exists)()
                if not channel_exists:
                    logger.error(f"Channel with ID {self.channel_id} does not exist.")
                    await self.close(code=403)
                    return

                # Fetch the channel and check if the user is part of it
                channel = await sync_to_async(Channel.objects.get)(id=self.channel_id)
                is_user_in_channel = await sync_to_async(channel.users.filter(id=self.scope['user'].id).exists)()
                if not is_user_in_channel:
                    logger.error(f"User {self.scope['user']} does not have access to channel {self.channel_id}.")
                    await self.close(code=403)
                    return
            except Exception as e:
                logger.error(f"Error while verifying channel: {str(e)}")
                await self.close(code=403)
                return

            # Add to the group and accept connection
            self.group_name = f"chat_{self.channel_id}"
            self.channel_layer = get_channel_layer()

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

            logger.info(f"User {self.scope['user'].username} connected to channel {self.group_name}.")
        except Exception as e:
            logger.error(f"Error during connection: {str(e)}")
            await self.close()


    async def disconnect(self, close_code):
        try:
            # Remove the WebSocket connection from the group
            self.channel_layer = get_channel_layer()
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            logger.info(f"User disconnected from channel {self.group_name}.")
        except Exception as e:
            logger.error(f"Error during disconnection: {str(e)}")

    async def receive(self, text_data):
        try:
            from .models import Channel, Message
            # Parse the incoming JSON message
            data = json.loads(text_data)
            message = data.get('message', None)
            
            if not message:
                raise ValueError("Invalid data format: 'message' field is required.")

            # Check if the user is authenticated
            if not self.scope['user'].is_authenticated:
                await self.send(text_data=json.dumps({
                    'error': 'User not authenticated.'
                }))
                return

            # Save the message to the database
            channel = await sync_to_async(Channel.objects.get)(id=self.channel_id)
            sender = self.scope['user']
            await sync_to_async(Message.objects.create)(
                sender=sender,
                channel=channel,
                text=message
            )

            # Broadcast the message to the group
            self.channel_layer = get_channel_layer()
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username,
                }
            )
        except ObjectDoesNotExist:
            await self.send(text_data=json.dumps({
                'error': 'Invalid channel ID.'
            }))
        except ValueError as ve:
            await self.send(text_data=json.dumps({
                'error': str(ve)
            }))
        except Exception as e:
            logger.error(f"Error during message receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred while processing your request.'
            }))

    async def chat_message(self, event):
        try:
            # Send the message to WebSocket
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender': event['sender'],
            }))
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {str(e)}")
