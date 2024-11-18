from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    is_moderator = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

       
User = get_user_model()
       
        
class Channel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='channels')


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
