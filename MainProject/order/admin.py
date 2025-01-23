from django.contrib import admin
from .models import Order,OrderDetails

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_uuid', 'user', 'status', 'order_on', 'total']
    list_filter = ['status', 'order_on']
    search_fields = ['user__username', 'order_uuid', 'status', 'order_on', 'total']

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'product', 'quantity', 'price']
    list_filter = ['product', 'quantity']
    search_fields = ['order_id__order_uuid', 'product__name', 'quantity', 'price']
