# packages/views.py
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Package, Category, Wishlist, Review, Discount
from django.urls import reverse
from django.contrib import messages

class PackageListView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'
    paginate_by = 9

    def get_queryset(self):
        queryset = Package.objects.all()  # Remove is_active filter
        category_slug = self.request.GET.get('category')
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        sort_by = self.request.GET.get('sort')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_sort'] = self.request.GET.get('sort')
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
    template_name = 'packages/wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
# Package Views
class PackageDetailView(DetailView):
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'
    slug_url_kwarg = 'slug'  # تحديد اسم المعامل في URL

    def get_object(self, queryset=None):
        # التأكد من أن الباقة نشطة
        return get_object_or_404(Package, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = self.get_object()
        # إضافة معلومات إضافية للسياق
        context['related_packages'] = Package.objects.filter(
            category=package.category
        ).exclude(id=package.id)[:3]
        context['in_wishlist'] = Wishlist.objects.filter(
            user=self.request.user,
            package=package
        ).exists() if self.request.user.is_authenticated else False
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


# Search View
class PackageSearchView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Package.objects.filter(name__icontains=query)