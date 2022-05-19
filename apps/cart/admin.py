from django.contrib import admin

# local imports
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'items_count', 'get_amount', 'created']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'quantity']
    # readonly_fields = ['item', 'quantity', 'amount']
