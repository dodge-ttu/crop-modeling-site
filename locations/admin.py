from django.contrib import admin
from .models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'site_id', 'is_published', 'post_date')
    list_display_links = ('site_id', 'name')
    list_editable = ('is_published',) # make checkboxes editable
    search_fields = ('name', 'description')
    list_per_page = 50


admin.site.register(Location, LocationAdmin)
