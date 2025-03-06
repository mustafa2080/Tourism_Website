from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from .models import Visitor, BookingAnalysis

def dashboard(request):
    # إحصائيات الحجوزات
    total_bookings = BookingAnalysis.objects.aggregate(total_bookings=Sum('total_bookings'))['total_bookings'] or 0
    total_revenue = BookingAnalysis.objects.aggregate(total_revenue=Sum('total_revenue'))['total_revenue'] or 0
    average_booking_price = total_revenue / total_bookings if total_bookings > 0 else 0

    # إحصائيات الزوار
    total_visitors = Visitor.objects.count()
    total_visits = Visitor.objects.aggregate(total_visits=Sum('visit_count'))['total_visits'] or 0
    average_visit_duration = Visitor.objects.aggregate(avg_duration=Avg('visit_duration'))['avg_duration'] or 0
    most_used_device = Visitor.objects.values('device_type').annotate(count=Count('device_type')).order_by('-count').first()
    most_used_device = most_used_device['device_type'] if most_used_device else "غير معروف"

    # تحليل الحجوزات
    bookings_by_status = {}
    bookings_by_destination = {}
    bookings_by_month = {}

    for booking in BookingAnalysis.objects.all():
        if booking.bookings_by_status:
            for status, count in booking.bookings_by_status.items():
                bookings_by_status[status] = bookings_by_status.get(status, 0) + count
        if booking.bookings_by_destination:
            for destination, count in booking.bookings_by_destination.items():
                bookings_by_destination[destination] = bookings_by_destination.get(destination, 0) + count
        if booking.bookings_by_month:
            for month, count in booking.bookings_by_month.items():
                bookings_by_month[month] = bookings_by_month.get(month, 0) + count

    # الوجهة الأكثر شعبية
    most_popular_destination = max(bookings_by_destination, key=bookings_by_destination.get, default="غير معروف")

    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'average_booking_price': round(average_booking_price, 2),
        'total_visitors': total_visitors,
        'total_visits': total_visits,
        'average_visit_duration': f"{average_visit_duration:.2f} دقائق",
        'most_used_device': most_used_device,
        'bookings_by_status': bookings_by_status,
        'bookings_by_destination': bookings_by_destination,
        'bookings_by_month': bookings_by_month,
        'most_popular_destination': most_popular_destination,
    }

    return render(request, 'analytics/dashboard.html', context)