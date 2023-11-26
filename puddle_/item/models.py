from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Se requiere dirección de correo electrónico")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

# Rest of the models
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta: 
        ordering = ("name",)
        verbose_name_plural = "Categories"
    

    def __str__(self):
        return self.name

class Item(models.Model):
    Category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey('item.CustomUser', related_name="items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.OneToOneField('item.CustomUser', related_name="cart", on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.user.email}"

    def get_cart_total(self):
        total = 0
        for cart_item in self.cart_items.all():
            total += cart_item.get_item_total()
        return total



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"

    def get_item_total(self):
        return self.item.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey('item.CustomUser', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_finalized = models.BooleanField(default=False)
    total = models.FloatField(default=0.0)  # Nuevo campo para almacenar el total
    created_at = models.DateTimeField(auto_now_add=True)

    def recalculate_total(self):
        self.total = sum(item.get_item_total() for item in self.order_items.all())
        self.save()

    def __str__(self):
        status = "Finalizada" if self.is_finalized else "Pendiente"
        return f"Orden de {self.user.email} - {status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} - Cantidad: {self.quantity}"

    def get_item_total(self):
        return self.quantity * self.item.price


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.address}, {self.city}, {self.country}, {self.zip_code}"



