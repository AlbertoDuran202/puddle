from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _
from item.models import Cart, CartItem, Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User


class CartInline(admin.StackedInline):
    model = Cart
    extra = 0
    fk_name = "user"

class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 0
    fk_name = "cart"

class OrderInline(admin.StackedInline):
    model = Order
    extra = 0
    fk_name = "user"

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    fk_name = "order"

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    fk_name = "order"

class UserAdmin(DefaultUserAdmin):
    inlines = DefaultUserAdmin.inlines + (OrderInline, ShippingAddressInline, OrderItemInline, CartInline, CartItemInline)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")

admin.site.register(User, UserAdmin)

