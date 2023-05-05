from django.contrib import admin
from .models import category
from .models import Item, Order,OrderItem,ShippingAddress
# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(category)
admin.site.register(Item)