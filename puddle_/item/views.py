from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Cart, CartItem

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(Category=item.Category, is_sold=False).exclude(pk=item.pk)[:4]
    in_cart = False

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        in_cart = cart.cart_items.filter(item=item).exists()

    return render(request, "item/item_detail.html", {"item": item, "related_items": related_items, "in_cart": in_cart})

def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("item:detail", pk=pk) # Cambia esta vista al nombre de la vista donde quieras redirigir al usuario.

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item=item)
    cart_item.quantity -= 1

    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()

    return redirect("item:detail", pk=pk) # Cambia esta vista al nombre de la vista donde quieras redirigir al usuario.ambia esta vista al nombre de la vista donde quieras redirigir al usuario.


@login_required
def view_cart(request):
    cart = request.user.cart
    cart_items = cart.cart_items.all()
    cart_total = cart.get_cart_total()
    return render(request, 'item/cart.html', {'cart_items': cart_items, 'total': cart_total})

@login_required
def update_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item=item)
    quantity = int(request.POST.get("quantity"))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("item:view_cart")


@login_required
def checkout(request):
    # Aquí va tu lógica de proceso de pago
    return render(request, "item/checkout.html")
