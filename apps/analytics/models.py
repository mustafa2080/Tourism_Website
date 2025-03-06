# analytics/models.py
from django.db import models
from django.conf import settings

class Visitor(models.Model):
    ip_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.CharField(max_length=200, blank=True, null=True)
    referrer = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # الحقول الجديدة
    page_visited = models.CharField(max_length=200, blank=True, null=True)  # الصفحة التي تمت زيارتها
    visit_duration = models.DurationField(blank=True, null=True)  # مدة الزيارة
    device_type = models.CharField(max_length=50, blank=True, null=True)  # نوع الجهاز
    operating_system = models.CharField(max_length=50, blank=True, null=True)  # نظام التشغيل
    browser_language = models.CharField(max_length=50, blank=True, null=True)  # لغة المتصفح
    visit_count = models.PositiveIntegerField(default=1)  # عدد الزيارات

    class Meta:
        app_label = 'analytics'

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"
    
    def increment_visit_count(self):
        """زيادة عدد الزيارات عند كل زيارة جديدة."""
        self.visit_count += 1
        self.save()

    def update_visit_duration(self, duration):
        """تحديث مدة الزيارة."""
        self.visit_duration = duration
        self.save()

# apps/analytics/models.py
class BookingAnalysis(models.Model):
    total_bookings = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bookings_by_status = models.JSONField(default=dict)
    bookings_by_destination = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    # الحقول الجديدة
    average_booking_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # متوسط سعر الحجز
    active_bookings = models.PositiveIntegerField(default=0)  # الحجوزات النشطة
    cancelled_bookings = models.PositiveIntegerField(default=0)  # الحجوزات الملغاة
    most_popular_destination = models.CharField(max_length=100, blank=True, null=True)  # الوجهة الأكثر شعبية
    bookings_by_month = models.JSONField(default=dict)  # الحجوزات حسب الشهر

    class Meta:
        app_label = 'analytics'

    def __str__(self):
        return f"Booking Analysis - {self.timestamp}"
    
    def calculate_average_booking_price(self):
        """حساب متوسط سعر الحجز."""
        if self.total_bookings > 0:
            self.average_booking_price = self.total_revenue / self.total_bookings
            self.save()

    def update_most_popular_destination(self):
        """تحديث الوجهة الأكثر شعبية."""
        if self.bookings_by_destination:
            self.most_popular_destination = max(
                self.bookings_by_destination, key=self.bookings_by_destination.get
            )
            self.save()