from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .jwt_custom import CustomTokenObtainPairView
from .registration import register
from .user_views import UserProfileView, ChangePasswordView

urlpatterns = [
    path("auth/register/", register, name="auth-register"),
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("auth/profile/", UserProfileView.as_view(), name="user-profile"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
]