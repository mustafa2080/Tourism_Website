from django.urls import path
from .views import (
    PackageListView, 
    PackageDetailView, 
    CategoryDetailView,
    WishlistAddView, 
    WishlistRemoveView, 
    WishlistListView,
    ReviewCreateView, 
    DiscountListView,
    PackageSearchView
)

app_name = 'packages'

urlpatterns = [
    path('packages/', PackageListView.as_view(), name='package_list'),
    path('package/<slug:slug>/', PackageDetailView.as_view(), name='package_detail'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('wishlist/add/<int:package_id>/', WishlistAddView.as_view(), name='wishlist_add'),
    path('wishlist/remove/<slug:slug>/', WishlistRemoveView.as_view(), name='wishlist_remove'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist_list'),
    path('package/<slug:slug>/review/', ReviewCreateView.as_view(), name='review_create'),
    path('discounts/', DiscountListView.as_view(), name='discount_list'),
    path('search/', PackageSearchView.as_view(), name='package_search'),
]