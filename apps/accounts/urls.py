from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    ProfileView, 
    ProfileEditView, 
    GoogleLoginView, 
    FacebookLoginView, 
    SettingsView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('facebook/login/', FacebookLoginView.as_view(), name='facebook_login'),
    path('settings/', SettingsView.as_view(), name='settings'),
]