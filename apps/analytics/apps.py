# apps/analytics/apps.py
from django.apps import AppConfig

class AnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analytics'  # لو الـ Application جوا مجلد apps