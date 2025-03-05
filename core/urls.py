from django.contrib import admin
from django.urls import path
from .swagger import doc_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += doc_urlpatterns
