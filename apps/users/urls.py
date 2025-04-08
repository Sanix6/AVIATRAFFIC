from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'user', PersonalView, basename='auth')

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='auth-register'),
    path('', include(router.urls)),
]