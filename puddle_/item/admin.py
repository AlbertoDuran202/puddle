from django.contrib import admin
from .models import Category, Item, Order, OrderItem, ShippingAddress

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    fk_name = "order"

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    fk_name = "order"

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, ShippingAddressInline)

admin.site.register(ShippingAddress)
admin.site.register(Order, OrderAdmin)  # Mueve esta línea aquí y elimina la línea duplicada 'admin.site.register(Order)'
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Item)

    