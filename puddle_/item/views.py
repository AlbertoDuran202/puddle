from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Cart, CartItem, ShippingAddress, Order
from .forms import ShippingAddressForm
from django.contrib import messages


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

    return redirect("item:detail", pk=pk)

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

    return redirect("item:detail", pk=pk)

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
def create_order(request):
    order = Order.objects.create(user=request.user)
    request.session['order_id'] = order.id
    # Añade la lógica adicional que necesites para la creación de pedidos aquí
    return redirect("item:create_shipping_address")

@login_required
def create_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            order_id = request.session.get('order_id')
            if order_id is not None:
                order = Order.objects.get(pk=order_id)
                shipping_address.order = order
            shipping_address.user = request.user
            shipping_address.save()
            messages.success(request, 'La dirección de envío se ha guardado con éxito.')
            return redirect('item:checkout')
    else:
        form = ShippingAddressForm()
    return render(request, 'item/create_shipping_address.html', {'form': form})


