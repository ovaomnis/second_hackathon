from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from applications.account.views import (RegisterAPIView, ActivationAPIView, ChangePasswordAPIView, ForgotPasswordAPIView, ForgotPasswordResetAPIView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uuid:code>/', ActivationAPIView().as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view()),
    path('reset-password/', ForgotPasswordResetAPIView.as_view()),

    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
