from django.urls import path
from .views import UserRegisterView, ChannelListView, MessageListView, BlockUserView, PromoteToModeratorView

urlpatterns = [
    
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('channels/', ChannelListView.as_view(), name='channel_list'),
    path('messages/', MessageListView.as_view(), name='message_list'),  
    path('block_user/', BlockUserView.as_view(), name='block_user'), 
    path('promote/', PromoteToModeratorView.as_view(), name='promote_to_moderator'),

]
