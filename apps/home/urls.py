from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BaseView


router = DefaultRouter()
router.register(r'base', BaseView, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]