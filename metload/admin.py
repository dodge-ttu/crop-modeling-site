from django.contrib import admin
from .models import Obsset


class ObssetAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'datetime', 'temperature')
    list_filter = ('site_name',)


# class LocationAdmin(admin.ModelAdmin):
#     list_display = ('provider_id', 'service_provider', 'name', 'is_published', 'post_date')
#     list_display_links = ('provider_id', 'name')
#     list_editable = ('is_published',) # make checkboxes editable
#     search_fields = ('name', 'description')
#     list_per_page = 50


admin.site.register(Obsset, ObssetAdmin)
