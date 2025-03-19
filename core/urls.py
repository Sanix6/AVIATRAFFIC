from django.contrib import admin
from django.urls import path, include
from .swagger import doc_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.home.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path("monitor", include("django_prometheus.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += doc_urlpatterns
