from django.contrib import admin
from .models import Product, Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order
    inlines = [
        OrderItemInline,
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register([Product, OrderItem])