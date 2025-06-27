from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BaseView, FAQDetailAPIView, FAQListAPIView


router = DefaultRouter()
router.register(r'', BaseView, basename='auth'),


urlpatterns = [
    path('', include(router.urls)),
    path('faq/', FAQListAPIView.as_view(), name='faq-list'),
    path('faq/<slug:slug>/', FAQDetailAPIView.as_view(), name='faq-detail'),
]