from django.contrib import admin
from .models import Product, Cart, Wishlist

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'selling_price', 'discounted_price']
    list_filter = ['category']
    search_fields = ['name','category']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_filter = ['user', 'product']
    search_fields = ['user__username', 'product__name']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'added_at']
    list_filter = ['user', 'product', 'added_at']
    search_fields = ['user__username', 'product__name']
