from django.db import models
from django.conf import settings
from apps.packages.models import Package
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'مؤكد'),
        ('cancelled', 'ملغي'),
    ]
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package_bookings', null=True, blank=True)
    special_requests = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('bank', 'تحويل بنكي'),
        ('cash', 'نقدي'),
        ('card', 'بطاقة ائتمان')
    ],
        default='cash'  # Set a default value here
        )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey('destinations.Destination', on_delete=models.CASCADE)
    start_date = models.DateField()
    package = models.ForeignKey('packages.Package', on_delete=models.CASCADE, null=True, blank=True)
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'bookings'
    
    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"
    
    
    
# bookings/models.py
class BankPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'في انتظار التحويل'),
        ('completed', 'تم التحويل'),
        ('failed', 'فشل التحويل'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='bank_payment')
    bank_name = models.CharField(max_length=100, verbose_name='اسم البنك')
    account_holder = models.CharField(max_length=100, verbose_name='اسم صاحب الحساب')
    transaction_date = models.DateField(verbose_name='تاريخ التحويل')
    transaction_number = models.CharField(max_length=100, verbose_name='رقم التحويل')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ المحول')
    receipt_image = models.ImageField(upload_to='bank_receipts/', verbose_name='صورة الإيصال')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"دفع بنكي - {self.booking.user.username}"
    
    
    
class PaymobPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymob_order_id = models.CharField(max_length=100, blank=True, null=True)
    paymob_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"