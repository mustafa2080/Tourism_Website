# apps/analytics/utils.py
from django.db.models import Count, Sum
from apps.bookings.models import Booking
from apps.destinations.models import Destination
from .models import BookingAnalysis, Visitor

def analyze_bookings():
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0  # تأكد من وجود or 0
    bookings_by_status = Booking.objects.values('status').annotate(count=Count('id'))
    bookings_by_destination = Booking.objects.values('destination__name').annotate(count=Count('id'))

    BookingAnalysis.objects.create(
        total_bookings=total_bookings,
        total_revenue=total_revenue,  # تأكد من وجود قيمة هنا
        bookings_by_status={item['status']: item['count'] for item in bookings_by_status},
        bookings_by_destination={item['destination__name']: item['count'] for item in bookings_by_destination},
    )

def analyze_visitors():
    total_visitors = Visitor.objects.count()
    visitors_by_country = Visitor.objects.values('country').annotate(count=Count('id'))
    visitors_by_city = Visitor.objects.values('city').annotate(count=Count('id'))

    return {
        'total_visitors': total_visitors,
        'visitors_by_country': {item['country']: item['count'] for item in visitors_by_country},
        'visitors_by_city': {item['city']: item['count'] for item in visitors_by_city},
    }