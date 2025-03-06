from django.contrib import admin
from .models import Package, Category, Wishlist, Discount, Review
from apps.bookings.models import Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'category', 'destination', 'is_featured']
    list_filter = ['category', 'destination', 'difficulty', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'price']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'created_at']
    list_filter = ['user', 'package']
    search_fields = ['user__username', 'package__name']
    date_hierarchy = 'created_at'

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['package', 'percentage', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'package']
    search_fields = ['package__name']
    date_hierarchy = 'start_date'
    list_editable = ['is_active']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'rating', 'created_at']
    list_filter = ['rating', 'package']
    search_fields = ['user__username', 'package__name', 'comment']
    date_hierarchy = 'created_at'
    

# إلغاء تسجيل النموذج إذا كان مسجلًا مسبقًا
admin.site.unregister(Package)
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'category', 'destination')
    search_fields = ('name', 'description')
    list_filter = ('category', 'destination', 'difficulty')