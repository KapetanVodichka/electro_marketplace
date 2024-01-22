from django.contrib import admin

from market.models import NetworkElement


class NetworkElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'supplier', 'debt_to_supplier', 'created_at')
    list_display_links = ('name', 'supplier')
    list_filter = ('contacts__country', 'contacts__city')
    search_fields = ('name', 'contacts__city')

    actions = ['clear_debt']

    def clear_debt(self, request, queryset):
        queryset.update(debt_to_supplier=0)


admin.site.register(NetworkElement, NetworkElementAdmin)