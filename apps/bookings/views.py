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
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from apps.analytics.models import BookingAnalysis

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    pk_url_kwarg = 'booking_id'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class CreateBookingView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/create_booking.html'
    success_url = reverse_lazy('bookings:my_bookings')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.package = get_object_or_404(Package, id=self.kwargs['package_id'])
        form.instance.total_price = form.instance.package.price * form.cleaned_data['number_of_persons']
        response = super().form_valid(form)
        
        # Create booking analysis
        BookingAnalysis.objects.create(
            total_bookings=1,
            total_revenue=form.instance.total_price,
            bookings_by_status={form.instance.status: 1},
            bookings_by_destination={form.instance.package.destination.name: 1},
            bookings_by_month={form.instance.booking_date.strftime('%B'): 1},
        )
        
        messages.success(self.request, 'تم إنشاء الحجز بنجاح!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package'] = get_object_or_404(Package, id=self.kwargs['package_id'])
        return context

class ConfirmBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'تم تأكيد الحجز بنجاح! يرجى إكمال عملية الدفع.')
        return redirect('bookings:bank_payment', booking_id=booking.id)

class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'تم إلغاء الحجز بنجاح.')
        else:
            messages.error(request, 'لا يمكن إلغاء الحجز في حالته الحالية.')
        return redirect('bookings:my_bookings')

class BankPaymentView(LoginRequiredMixin, FormView):
    template_name = 'bookings/bank_payment.html'
    form_class = BankPaymentForm
    
    def get_success_url(self):
        return reverse_lazy('bookings:booking_detail', kwargs={'booking_id': self.kwargs['booking_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = get_object_or_404(Booking, id=self.kwargs['booking_id'], user=self.request.user)
        return context

    def form_valid(self, form):
        booking = get_object_or_404(Booking, id=self.kwargs['booking_id'], user=self.request.user)
        payment = form.save(commit=False)
        payment.booking = booking
        payment.amount = booking.total_price
        payment.save()
        
        booking.status = 'confirmed'
        booking.save()
        
        messages.success(self.request, 'تم تسجيل الدفع بنجاح!')
        return super().form_valid(form)

class PaymobPaymentView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        try:
            auth_token = get_paymob_auth_token()
            order_id = create_paymob_order(booking, auth_token)
            payment_key = get_payment_key(auth_token, order_id, booking)
            
            PaymobPayment.objects.create(
                user=request.user,
                booking=booking,
                amount=booking.total_price,
                paymob_order_id=order_id,
                payment_status='pending'
            )
            
            return redirect(f"https://accept.paymob.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_key}")
        except Exception as e:
            messages.error(request, f"فشلت عملية الدفع: {str(e)}")
            return redirect('bookings:booking_detail', booking_id=booking.id)

# Keep the paymob_webhook view as is since it needs to be function-based for CSRF exemption
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



# Booking Views
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['number_of_persons']
    template_name = 'packages/booking_form.html'

    def form_valid(self, form):
        package = get_object_or_404(Package, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        form.instance.package = package
        form.instance.total_price = package.price * form.instance.number_of_persons
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('packages:booking_detail', kwargs={'booking_id': self.object.id})

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'packages/booking_detail.html'
    context_object_name = 'booking'
