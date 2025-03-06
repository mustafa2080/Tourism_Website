from django.shortcuts import render, redirect
from django.contrib import messages
from apps.destinations.models import Destination
from apps.blog.models import Post
from apps.core.forms import ContactForm  # تعديل الاستيراد هنا

def home(request):
    featured_destinations = Destination.objects.all()[:6]
    latest_posts = Post.objects.all()[:3]
    
    context = {
        'featured_destinations': featured_destinations,
        'latest_posts': latest_posts
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إرسال رسالتك بنجاح!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

def faq(request):
    return render(request, 'core/faq.html')

def terms(request):
    return render(request, 'core/terms.html')


def some_view(request):
    messages.success(request, 'تمت العملية بنجاح!')
    return redirect('home')