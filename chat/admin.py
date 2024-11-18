from django.contrib import admin
from .models import User, Channel, Message

# Register the models in the admin interface
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_moderator', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_moderator', 'is_active', 'is_staff')

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'channel', 'text', 'timestamp')
    search_fields = ('text',)
    list_filter = ('timestamp',)
