from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth import get_user_model
from item.models import Cart, CartItem, Order, OrderItem, ShippingAddress

# Obtén el modelo de usuario actual
User = get_user_model()

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

class CustomUserAdmin(DefaultUserAdmin):
    # Define las configuraciones del admin para CustomUser
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    inlines = [OrderInline, ShippingAddressInline, OrderItemInline, CartInline, CartItemInline]

# Registra el modelo CustomUser con la clase CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
