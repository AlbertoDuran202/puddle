from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Cart, CartItem, ShippingAddress, Order, OrderItem
from .forms import ShippingAddressForm
from django.contrib import messages
import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import logging

# Crea un logger para tu aplicación
logger = logging.getLogger(__name__)


# Configuración de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY



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

    # Crear una orden tentativa si no existe
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False, is_finalized=False)
    OrderItem.objects.get_or_create(order=order, item=item, defaults={'quantity': 1})

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

        # Actualizar el OrderItem correspondiente en la orden tentativa
        order = Order.objects.filter(user=request.user, is_paid=False, is_finalized=False).first()
        if order:
            order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
            order_item.quantity = quantity
            order_item.save()
    else:
        cart_item.delete()
        # Eliminar el OrderItem correspondiente
        order = Order.objects.filter(user=request.user, is_paid=False, is_finalized=False).first()
        if order:
            OrderItem.objects.filter(order=order, item=item).delete()

    return redirect("item:view_cart")




@login_required
def create_order(request):
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False, defaults={'user': request.user})
    request.session['order_id'] = order.id
    print("Order ID set in session:", request.session['order_id'])  # Impresión de depuración
    return redirect("item:create_shipping_address")



@login_required
def create_shipping_address(request):
    print("Iniciando create_shipping_address")  # Mensaje de depuración

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            order_id = request.session.get('order_id')

            if order_id is not None:
                print(f"Order ID obtenido: {order_id}")  # Mensaje de depuración
                try:
                    order = Order.objects.get(pk=order_id)
                    shipping_address.order = order
                except Order.DoesNotExist:
                    messages.error(request, 'Pedido no encontrado.')
                    return redirect('item:view_cart')

                shipping_address.user = request.user
                try:
                    shipping_address.save()
                    messages.success(request, 'La dirección de envío se ha guardado con éxito.')
                    return redirect('item:checkout')
                except Exception as e:
                    print(f"Error al guardar la dirección de envío: {e}")  # Mensaje de depuración
                    messages.error(request, 'Error al guardar la dirección de envío.')
            else:
                print("Order ID no se encuentra en la sesión")  # Mensaje de depuración
                messages.error(request, 'No se pudo encontrar el ID del pedido.')
                return redirect('item:view_cart')
    else:
        form = ShippingAddressForm()

    return render(request, 'item/create_shipping_address.html', {'form': form})


@login_required
def initiate_checkout(request):
    # Buscar un pedido existente que no esté pagado
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False, defaults={'user': request.user})
    request.session['order_id'] = order.id

    # Verificar si ya existe una dirección de envío para el pedido
    shipping_address = ShippingAddress.objects.filter(order=order).first()
    if shipping_address:
        return redirect('item:checkout')
    else:
        return redirect('item:create_shipping_address')


 # Asegúrate de importar los modelos necesarios


@login_required
def checkout(request):
    # Configura la clave de API de Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Obtener la orden tentativa
    order = Order.objects.filter(user=request.user, is_paid=False, is_finalized=False).first()

    if not order:
        # Redirigir al carrito si no hay una orden tentativa
        return redirect('item:view_cart')

    # Obtiene los items de la orden tentativa
    order_items = order.order_items.all()
    cart_total = sum(item.get_item_total() for item in order_items)

    # Convertir el total del carrito a centavos para Stripe
    cart_total_cents = int(cart_total * 100)

    # Obtener la dirección de envío si existe
    shipping_address = ShippingAddress.objects.filter(order=order).first()

    # Crea un PaymentIntent con Stripe
    intent = stripe.PaymentIntent.create(
        amount=cart_total_cents,
        currency='mxn',
        payment_method_types=['card']
    )

    context = {
        'order_items': order_items,
        'total': cart_total,
        'shipping_address': shipping_address,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'clientSecret': intent.client_secret
    }

    return render(request, 'item/checkout.html', context)



