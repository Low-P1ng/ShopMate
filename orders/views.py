from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import AddressForm
from .models import Address, Order, OrderItem
from cart.cart import Cart

@login_required
def add_address(request):
    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        address = None

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address saved successfully.")
            return redirect("checkout")
    else:
        form = AddressForm(instance=address)

    return render(request, 'orders/add_address.html', {'form': form})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty.")
        return redirect('index')

    address = None
    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            address = None

    return render(request, 'orders/checkout.html', {'address': address, 'cart': cart})

def place_order(request):
    order_success = False
    if request.method == "POST":
        cart = Cart(request)
        if len(cart) == 0:
            return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)
            
        total_amount = cart.get_total_price()

        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, total_amount=total_amount)
        else:
            order = Order.objects.create(user=None, total_amount=total_amount)

        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['qty'])

        cart.clear()
        order_success = True

    return JsonResponse({'success': order_success})

def order_success(request):
    return render(request, 'orders/order-success.html')

def order_failed(request):
    return render(request, 'orders/order-failed.html')