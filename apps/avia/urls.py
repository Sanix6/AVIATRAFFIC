from django.urls import path
from apps.avia.views import *

urlpatterns = [
    path("search-ticket/", SearchTicketView.as_view()),
    path("raceinfo/", RaceInfoView.as_view()),
    path("booking/", BookingView.as_view()),
    path("booking-detail/", BookingDetail.as_view()),
    path("booking/cancel/", BookingCancelView.as_view())
]