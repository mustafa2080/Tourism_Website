# packages/views.py
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Package, Category, Wishlist, Review, Discount, Package
from django.urls import reverse
from django.contrib import messages  # أضف هذا الاستيراد
from apps.bookings.models import Booking


class PackageListView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # التصفية حسب الفئة (إذا تم تمريرها)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # الترتيب (إذا تم تمريره)
        sort = self.request.GET.get('sort')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'duration':
            queryset = queryset.order_by('duration')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_sort'] = self.request.GET.get('sort')
        
        # إضافة الباقات ذات الصلة (إذا كانت هناك فئة محددة)
        category = self.request.GET.get('category')
        if category:
            context['related_packages'] = Package.objects.filter(
                category__slug=category
            ).exclude(id__in=[p.id for p in context['packages']])[:3]
        else:
            context['related_packages'] = Package.objects.none()
        
        return context

class CategoryDetailView(ListView):
    model = Package
    template_name = 'packages/category_detail.html'
    context_object_name = 'packages'
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Package.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    
    # Wishlist Views
class WishlistAddView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        package = get_object_or_404(Package, id=self.kwargs['package_id'])
        Wishlist.objects.get_or_create(user=self.request.user, package=package)
        messages.success(request, 'تمت الإضافة إلى المفضلة بنجاح')
        return redirect('packages:package_detail', slug=package.slug)

class WishlistRemoveView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        package = get_object_or_404(Package, slug=slug)
        Wishlist.objects.filter(user=self.request.user, package=package).delete()
        messages.success(request, 'تم الحذف من المفضلة بنجاح')
        return redirect('packages:wishlist_list')

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'packages/wishlist_list.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
# Package Views
class PackageDetailView(DetailView):
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # جلب الحجوزات المرتبطة بالباقة باستخدام related_name
        context['bookings'] = self.object.booking_set.all()
        return context

# Review Views
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'packages/review_form.html'

    def form_valid(self, form):
        package = get_object_or_404(Package, slug=self.kwargs['slug'])
        
        if Review.objects.filter(user=self.request.user, package=package).exists():
            messages.error(self.request, 'لقد قمت بتقييم هذه الباقة مسبقًا!')
            return redirect('packages:package_detail', slug=package.slug)
        
        form.instance.user = self.request.user
        form.instance.package = package
        messages.success(self.request, 'تمت إضافة التقييم بنجاح!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('packages:package_detail', kwargs={'slug': self.kwargs['slug']})
    
# Discount Views
class DiscountListView(ListView):
    model = Discount
    template_name = 'packages/discount_list.html'
    context_object_name = 'discounts'

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

# Search View
class PackageSearchView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Package.objects.filter(name__icontains=query)
    
    
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'packages/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    

class CancelBookingView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        booking_id = kwargs.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        if booking.status == 'pending' or booking.status == 'confirmed':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'تم إلغاء الحجز بنجاح.')
        else:
            messages.error(request, 'لا يمكن إلغاء الحجز في حالته الحالية.')
        
        return redirect('packages:booking_list')  # أو أي صفحة أخرى تريد التوجيه إليها