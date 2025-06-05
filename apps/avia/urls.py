from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.avia.views import *

router = DefaultRouter()
router.register(r'', AviaParamsView, basename='avia')

urlpatterns = [
    path('', include(router.urls)),
    path("search-ticket/", SearchTicketView.as_view(), name="sirena-proxy"),
    path('cities/', ConnectedCitiesView.as_view(), name='cities'),

]