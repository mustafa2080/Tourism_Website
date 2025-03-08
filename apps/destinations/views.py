from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from apps.destinations.models import Destination, Category  # استخدم المسار الكامل
from apps.packages.models import Package  # استيراد نموذج Package
from django.db.models import Q

def destination_list(request):
    destinations = Destination.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    paginator = Paginator(destinations, 9)  # 9 وجهات في كل صفحة
    
    page = request.GET.get('page')
    destinations = paginator.get_page(page)
    
    return render(request, 'destinations/destination_list.html', {
        'destinations': destinations,
        'categories': categories
    })

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    
    # Get packages for this destination
    packages = Package.objects.filter(destination=destination)
    
    # Get similar destinations
    similar_destinations = Destination.objects.filter(
        location=destination.location
    ).exclude(id=destination.id)[:3]
    
    context = {
        'destination': destination,
        'packages': packages,
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

def destination_search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    destinations = Destination.objects.all()
    
    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category:
        destinations = destinations.filter(category__slug=category)
    
    categories = Category.objects.all()
    
    return render(request, 'destinations/destination_list.html', {
        'destinations': destinations,
        'categories': categories,
    })
