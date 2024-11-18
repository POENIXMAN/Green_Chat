from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Import JWT views
from chat.views import UserRegisterView  # Import the UserRegisterView

def root_view(request):
    return JsonResponse({
        "message": "Welcome to Green Chat API",
        "endpoints": {
            "Authentication": [
                {"description": "Register a new user", "path": "/api/register/", "method": "POST"},
                {"description": "Obtain JWT tokens", "path": "/api/token/", "method": "POST"},
                {"description": "Refresh JWT tokens", "path": "/api/token/refresh/", "method": "POST"}
            ],
            "Chat Management": [
                {"description": "List channels", "path": "/api/chat/channels/", "method": "GET"},
                {"description": "Create a channel", "path": "/api/chat/channels/", "method": "POST"},
                {"description": "List messages in a channel", "path": "/api/chat/messages/<channel_id>/", "method": "GET"},
                {"description": "Send a message to a channel", "path": "/ws/chat/<channel_id>/?token=<access_token>", "method": "WebSocket"},
                {"description": "Block a user in a channel", "path": "/api/chat/block_user/", "method": "POST"}
            ],
            "General": [
                {"description": "Admin panel", "path": "/admin/", "method": "GET"},
                {"description": "API root", "path": "/", "method": "GET"}
            ]
        }
    })


urlpatterns = [
    path('', root_view),  # Root URL
    path('admin/', admin.site.urls),
    path('api/register/', UserRegisterView.as_view(), name='user_register'),  # Correctly include /api/register/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh token
    path('api/chat/', include('chat.urls')),  # Include chat app routes
]
