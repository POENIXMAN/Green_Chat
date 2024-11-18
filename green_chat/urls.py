from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Import JWT views
from chat.views import UserRegisterView  # Import the UserRegisterView

def root_view(request):
    return JsonResponse({
        "message": "Welcome to Green Chat API",
        "endpoints": [
            "/admin/",
            "/api/register/",
            "/api/token/",
            "/api/token/refresh/",
            "/api/chat/channels/",
            "/api/chat/messages/",
            "/api/chat/block_user/"
        ]
    })

urlpatterns = [
    path('', root_view),  # Root URL
    path('admin/', admin.site.urls),
    path('api/register/', UserRegisterView.as_view(), name='user_register'),  # Correctly include /api/register/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh token
    path('api/chat/', include('chat.urls')),  # Include chat app routes
]
