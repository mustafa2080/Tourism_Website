# analytics/urls.py
from django.urls import path
from . import views

app_name = 'analytics'


urlpatterns = [
    path('dashboard/', views.dashboard, name='analytics_dashboard'),
]