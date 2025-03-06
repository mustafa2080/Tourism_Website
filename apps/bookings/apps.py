# apps/bookings/apps.py
from django.apps import AppConfig  # تأكد من وجود هذا السطر

class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bookings'  # تأكد من أن الاسم هنا مطابق لمسار التطبيق