# apps/destinations/apps.py
from django.apps import AppConfig  # تأكد من وجود هذا السطر

class DestinationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.destinations'  # تأكد من أن الاسم هنا مطابق لمسار التطبيق