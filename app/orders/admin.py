from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'tracking_number', 'created_at', 'updated_at', 'total_amount')
    list_filter = ('status', 'customer')
    search_fields = ('tracking_number', 'customer__first_name', 'customer__last_name')
    list_per_page = 20


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
