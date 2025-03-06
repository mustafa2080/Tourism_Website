from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.destination_list, name='destination_list'),
    path('<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('search/', views.search_destinations, name='search'),
    path('category/<slug:category_slug>/', views.destination_by_category, name='destination_by_category'),
]