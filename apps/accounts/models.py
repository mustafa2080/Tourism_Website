from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, default='profiles/default.png')
    
    class Meta:
        app_label = 'accounts'  # تحديد app_label يدويًا

    
    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    newsletter_subscription = models.BooleanField(default=False)
    preferred_currency = models.CharField(max_length=3, default='USD')
    travel_preferences = models.TextField(blank=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username