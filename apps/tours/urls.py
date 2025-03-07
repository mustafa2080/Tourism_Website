from django.urls import path
from . import views

app_name = 'tours'  # Add this to define the namespace

urlpatterns = [
    path('', views.TourListView.as_view(), name='list'),
    path('<int:pk>/', views.TourDetailView.as_view(), name='detail'),
    # ...other tour related URLs...
]
