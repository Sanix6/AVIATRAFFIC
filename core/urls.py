from django.contrib import admin
from django.urls import path, include
from .swagger import doc_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as ckeditor_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls')),
    path('base/', include('apps.home.urls')),
    path('avia/', include('apps.avia.urls')),
    path('api/ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/browse/', ckeditor_views.browse, name='ckeditor_browse'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += doc_urlpatterns
