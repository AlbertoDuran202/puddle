from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from item.models import Order, ShippingAddress

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0

class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    extra = 0

class UserAdmin(DefaultUserAdmin):
    inlines = DefaultUserAdmin.inlines + (OrderInline,)



