from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'user', PersonalView, basename='auth')

urlpatterns = [
    path('user/register', RegisterView.as_view(), name='auth-register'),
    path('user/login', LoginView.as_view(), name='auth-login'),
    path('user/confirm-code', ConfirmCodeView.as_view(), name='auth-confirm-email'),
    path('user/re-send/email', ReSendView.as_view(), name='auth-re-send'),
    path('', include(router.urls)),
]