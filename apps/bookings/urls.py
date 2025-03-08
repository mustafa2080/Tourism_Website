# bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='my_bookings'),
    path('create/<int:package_id>/', views.CreateBookingView.as_view(), name='create_booking'),
    path('<int:booking_id>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('confirm/<int:booking_id>/', views.ConfirmBookingView.as_view(), name='confirm_booking'),
    path('cancel/<int:booking_id>/', views.CancelBookingView.as_view(), name='cancel_booking'),
    path('webhook/', views.paymob_webhook, name='paymob_webhook'),
]