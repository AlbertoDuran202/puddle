from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class category (models.Model):
    name = models.CharField(max_length=255)

    class Meta: 
        ordering = ("name",)
        verbose_name_plural = "Categories"
    

    def __str__(self):
        return self.name

class Item(models.Model):
    Category = models.ForeignKey(category, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.OneToOneField(User, related_name="cart", on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.user.username}"

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







