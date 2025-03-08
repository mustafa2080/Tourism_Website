from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.destination_list, name='destination_list'),
    path('search/', views.destination_search, name='search'),
    path('<slug:slug>/', views.destination_detail, name='destination_detail'),  # Changed from pk to slug
]