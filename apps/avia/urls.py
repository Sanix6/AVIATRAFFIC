from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.avia.views import *

router = DefaultRouter()
router.register(r'avia', AviaParamsView, basename='avia')

urlpatterns = [
    path('', include(router.urls))
]