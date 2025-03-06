# destinations/admin.py
from django.contrib import admin
from .models import Destination

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    # list_filter = ('is_featured',)
    search_fields = ('name', 'location')

admin.site.register(Destination, DestinationAdmin)