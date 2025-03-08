# packages/models.py
from django.db import models
from apps.destinations.models import Destination
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse
from django.db.models import Avg
from decimal import Decimal  # أضف هذا الاستيراد في الأعلى

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=False)
    description = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

# packages/models.py
class Package(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'سهل'),
        ('moderate', 'متوسط'),
        ('hard', 'صعب'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="مدة الرحلة بالأيام")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='packages')
    destination = models.ForeignKey('destinations.Destination', on_delete=models.CASCADE, related_name='packages')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='moderate')
    image = models.ImageField(upload_to='packages/')
    included_services = models.TextField(help_text="الخدمات المتضمنة في الباقة")
    excluded_services = models.TextField(help_text="الخدمات غير المتضمنة", blank=True)
    itinerary = models.TextField(help_text="تفاصيل الرحلة يوم بيوم")
    max_persons = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bookings = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='package_bookings', null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('packages:package_detail', args=[self.slug])

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'package')
        verbose_name = "قائمة الرغبات"
        verbose_name_plural = "قوائم الرغبات"


class Discount(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='discounts')
    percentage = models.PositiveIntegerField(help_text="نسبة الخصم")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.percentage}% خصم على {self.package.name}"

    @property
    def discounted_price(self):
        """حساب السعر بعد الخصم."""
        # تحويل نسبة الخصم إلى Decimal
        discount_percentage = Decimal(self.percentage) / Decimal(100)
        # حساب السعر بعد الخصم
        return self.package.price * (Decimal(1) - discount_percentage)

    class Meta:
        verbose_name = "خصم"
        verbose_name_plural = "الخصومات"
        
        
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='destination_reviews')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name} - {self.rating} نجوم"

