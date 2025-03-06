from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from apps.destinations.models import Destination  # استخدم المسار الكامل
from apps.packages.models import Package  # استيراد نموذج Package

def destination_list(request):
    destinations = Destination.objects.all().order_by('-created_at')
    paginator = Paginator(destinations, 9)  # 9 وجهات في كل صفحة
    
    page = request.GET.get('page')
    destinations = paginator.get_page(page)
    
    return render(request, 'destinations/destination_list.html', {
        'destinations': destinations
    })

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    
    # جلب الرحلات المتاحة لهذه الوجهة
    packages = Package.objects.filter(destination=destination)
    
    # جلب وجهات مشابهة
    similar_destinations = Destination.objects.filter(
        location=destination.location
    ).exclude(id=destination.id)[:3]
    
    context = {
        'destination': destination,
        'packages': packages,  # إضافة قائمة الرحلات
        'similar_destinations': similar_destinations
    }
    return render(request, 'destinations/destination_detail.html', context)

def search_destinations(request):
    query = request.GET.get('q')
    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    destinations = Destination.objects.all()
    
    if query:
        destinations = destinations.filter(name__icontains=query)
    if location:
        destinations = destinations.filter(location__icontains=location)
    if min_price:
        destinations = destinations.filter(price__gte=min_price)
    if max_price:
        destinations = destinations.filter(price__lte=max_price)
        
    return render(request, 'destinations/search_results.html', {
        'destinations': destinations,
        'query': query
    })
    
    
def destination_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    destinations = Destination.objects.filter(category=category).order_by('-created_at')
    
    paginator = Paginator(destinations, 9)  # 9 وجهات في كل صفحة
    page = request.GET.get('page')
    destinations = paginator.get_page(page)
    
    return render(request, 'destinations/destination_by_category.html', {
        'destinations': destinations,
        'category': category
    })
