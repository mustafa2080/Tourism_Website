# bookings/views.py
from .forms import BankPaymentForm, BookingForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.bookings.models import Booking, BankPayment
from apps.destinations.models import Destination
from .utils import get_paymob_auth_token, create_paymob_order, get_payment_key
from .models import PaymobPayment
from django.conf import settings
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.packages.models import Package
from django.views.generic import ListView
from apps.analytics.models import BookingAnalysis

@login_required
def bank_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        form = BankPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_price
            payment.save()
            
            # تحديث حالة الحجز إلى "تم الدفع"
            booking.status = 'confirmed'
            booking.save()
            
            messages.success(request, 'تم تسجيل الدفع بنجاح!')
            return redirect('bookings:booking_detail', booking_id=booking.id)
        else:
            messages.error(request, 'حدث خطأ أثناء معالجة الدفع. يرجى التحقق من البيانات المدخلة.')
    else:
        form = BankPaymentForm(initial={'amount': booking.total_price})
    
    return render(request, 'bookings/bank_payment.html', {
        'form': form,
        'booking': booking
    })

@login_required
def confirm_payment(request, booking_id):
    if not request.user.is_staff:
        messages.error(request, 'غير مصرح لك بتأكيد الدفع')
        return redirect('bookings:booking_list')
        
    booking = get_object_or_404(Booking, id=booking_id)
    payment = get_object_or_404(BankPayment, booking=booking)
    
    payment.payment_status = 'completed'
    payment.save()
    
    booking.status = 'confirmed'
    booking.save()
    
    messages.success(request, 'تم تأكيد الدفع بنجاح')
    return redirect('bookings:booking_detail', booking_id=booking.id)



# bookings/views.py
def create_booking(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.total_price = package.price * form.instance.number_of_persons
            booking.save()

            # تسجيل بيانات الحجز في BookingAnalysis
            BookingAnalysis.objects.create(
                total_bookings=1,
                total_revenue=booking.total_price,
                bookings_by_status={booking.status: 1},
                bookings_by_destination={package.destination.name: 1},
                bookings_by_month={booking.booking_date.strftime('%B'): 1},
            )

            messages.success(request, 'تم إنشاء الحجز بنجاح!')
            return redirect('bookings:booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(initial={'package': package})
    
    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'package': package
    })
    

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # هنا هنغير حالة الحجز لـ "مؤكد"
    booking.status = 'confirmed'
    booking.save()
    
    # بعد التأكيد، نودي اليوزر لصفحة الدفع
    messages.success(request, 'تم تأكيد الحجز بنجاح! يرجى إكمال عملية الدفع.')
    return redirect('bookings:bank_payment', booking_id=booking.id)


@login_required
def paymob_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    try:
        # الحصول على token للتفويض
        auth_token = get_paymob_auth_token()
        
        # إنشاء طلب دفع
        order_id = create_paymob_order(booking, auth_token)
        
        # إنشاء مفتاح دفع
        payment_key = get_payment_key(auth_token, order_id, booking)
        
        # حفظ معلومات الدفع في قاعدة البيانات
        payment = PaymobPayment.objects.create(
            user=request.user,
            booking=booking,
            amount=booking.total_price,
            paymob_order_id=order_id,
            payment_status='pending'
        )
        
        # توجيه المستخدم إلى صفحة الدفع
        return redirect(f"https://accept.paymob.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_key}")
    
    except Exception as e:
        messages.error(request, f"فشلت عملية الدفع: {str(e)}")
        return redirect('bookings:booking_detail', booking_id=booking.id)
    
@csrf_exempt
def paymob_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # التحقق من HMAC (اختياري)
        hmac = data.get('hmac')
        if hmac != settings.PAYMOB_HMAC_SECRET:
            return HttpResponse(status=403)
        
        # تحديث حالة الدفع
        order_id = data.get('order')
        transaction_id = data.get('id')
        success = data.get('success')
        
        payment = PaymobPayment.objects.get(paymob_order_id=order_id)
        if success:
            payment.payment_status = 'completed'
            payment.paymob_transaction_id = transaction_id
            payment.save()
            
            # تحديث حالة الحجز
            booking = payment.booking
            booking.status = 'confirmed'
            booking.save()
        
        return HttpResponse(status=200)
    return HttpResponse(status=400)


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking
    })
    
    
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'pending' or booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'تم إلغاء الحجز بنجاح.')
    else:
        messages.error(request, 'لا يمكن إلغاء الحجز في حالته الحالية.')
    
    return redirect('bookings:booking_list')  # أو أي صفحة أخرى تريد التوجيه إليها


def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'packages/booking_list.html', {'bookings': bookings})