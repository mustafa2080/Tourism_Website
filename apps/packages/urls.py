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
    path('', PackageListView.as_view(), name='package_list'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist_list'),  # Move wishlist URLs before detail view
    path('wishlist/add/<int:package_id>/', WishlistAddView.as_view(), name='wishlist_add'),
    path('wishlist/remove/<slug:slug>/', WishlistRemoveView.as_view(), name='wishlist_remove'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('review/<slug:slug>/', ReviewCreateView.as_view(), name='review_create'),
    path('discounts/', DiscountListView.as_view(), name='discount_list'),
    path('search/', PackageSearchView.as_view(), name='package_search'),
    path('<slug:slug>/', PackageDetailView.as_view(), name='package_detail'),  # Move detail view to bottom
]