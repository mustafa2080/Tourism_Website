# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import UserProfile
from django.contrib.auth import get_user_model

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'
    }))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_image']
        

class NotificationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email_notifications', 'sms_notifications']
        
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['newsletter_subscription', 'preferred_currency', 'travel_preferences']
        
        
User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_image']