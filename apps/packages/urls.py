from django.urls import path
from .views import (
    PackageListView, PackageDetailView, CategoryDetailView,
    WishlistAddView, WishlistRemoveView, WishlistListView,
    ReviewCreateView, DiscountListView, BookingCreateView,
    BookingDetailView, PackageSearchView, BookingListView, CancelBookingView
)

app_name = 'packages'

urlpatterns = [
    path('', PackageListView.as_view(), name='package_list'),
    path('package/<slug:slug>/', PackageDetailView.as_view(), name='package_detail'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),

    # قائمة الرغبات
    path('wishlist/add/<int:package_id>/', WishlistAddView.as_view(), name='wishlist_add'),
    path('wishlist/remove/<slug:slug>/', WishlistRemoveView.as_view(), name='wishlist_remove'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist_list'),

    # التقييمات
    path('package/<slug:slug>/review/', ReviewCreateView.as_view(), name='review_create'),

    # الخصومات
    path('discounts/', DiscountListView.as_view(), name='discount_list'),

    # الحجوزات
    path('package/<slug:slug>/book/', BookingCreateView.as_view(), name='booking_create'),
    path('booking/<int:booking_id>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/cancel/<int:booking_id>/', CancelBookingView.as_view(), name='cancel_booking'),


    # البحث
    path('search/', PackageSearchView.as_view(), name='package_search'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),

]