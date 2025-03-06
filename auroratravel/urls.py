from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls'), name="home"),
    path('accounts/', include('apps.accounts.urls')),
    path('destinations/', include('apps.destinations.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('blog/', include('apps.blog.urls')),
    path('packages/', include('apps.packages.urls')),
    path('analytics/', include('apps.analytics.urls')),

    #path('api/', include('apps.api.urls')),  # لإضافة واجهة برمجة التطبيقات
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)