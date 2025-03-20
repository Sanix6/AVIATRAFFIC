from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class NoticeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'
    verbose_name = _('Уведомления')

    def ready(self):
        import apps.notifications.signals