# bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:package_id>/', views.create_booking, name='create_booking'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('payment/<int:booking_id>/', views.bank_payment, name='bank_payment'),  # تأكد من وجود هذا المسار
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('paymob/webhook/', views.paymob_webhook, name='paymob_webhook'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('paymob_payment/<int:booking_id>/', views.paymob_payment, name='paymob_payment'),  # إضافة هذا المسار
]