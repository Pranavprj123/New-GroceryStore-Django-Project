from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
import razorpay
from .models import  Order, OrderDetails
from product.models import Product
from accounts.models import Customer
from django.conf import settings
from razorpay import Client
import pkg_resources
import razorpay

@login_required
def checkout(request):
    user = request.user
    # Fetch customer address and cart items
    customer = Customer.objects.filter(user=user).first()
    cart_items = Cart.objects.filter(user=user)
    
    # Initialize amounts
    amount = Decimal('0.0')
    shipping_amount = Decimal('70.0')
    
    # Calculate total amount from cart items
    if cart_items.exists():
        amount = sum(item.quantity * item.product.selling_price for item in cart_items)
        total_amount = amount + shipping_amount
    else:
        total_amount = Decimal('0.0')
    
    # Razorpay integration
    razorpay_amount = int(total_amount * 100)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    razorpay_order = client.order.create({
        "amount": razorpay_amount,
        "currency": "INR",
        "payment_capture": "1"
    })
    
    context = {
        'customer': customer,
        'total_amount': total_amount,
        'razorpay_amount': razorpay_amount,
        'cart_items': cart_items,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'currency': "INR",
        'callback_url': request.build_absolute_uri(reverse('payment_handler'))  # Callback URL for payment handler
    }
    
    return render(request, 'order/checkout.html', context)


@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            # Get payment details from POST data
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Verify signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            try:
                client.utility.verify_payment_signature(params_dict)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

            # Get the authenticated user
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            # Get cart items
            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                return JsonResponse({'error': 'Cart is empty'}, status=400)

            # Calculate total amount
            total = sum(item.quantity * item.product.selling_price for item in cart_items)
            shipping_amount = Decimal('70.0')
            total_amount = total + shipping_amount

            # Create Order
            new_order = Order.objects.create(
                user=user,
                total=total_amount,
                razorpay_order_id=order_id,
                status='pending'
            )

            # Create OrderDetails for each cart item
            for item in cart_items:
                OrderDetails.objects.create(
                    order_id=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.quantity * item.product.selling_price
                )

            # Clear the cart after successful order
            cart_items.delete()

            # Redirect to order details page
            return redirect('order_details', order_id=new_order.order_uuid)

        except Exception as e:
            return JsonResponse({'error': f'Error processing payment: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def order_details(request, order_id):
    try:
        # Fetch the order and check ownership
        order = get_object_or_404(Order, order_uuid=order_id, user=request.user)
        # Fetch the order details (products) related to this order
        order_details = order.details.all()

        context = {
            'order': order,
            'order_details': order_details,
            'title': f'Order #{order.order_uuid}',
        }

        return render(request, 'order/order_detail.html', context)

    except Order.DoesNotExist:
        return render(request, 'order/order_not_found.html', {
            'error_message': 'Order not found or access denied.',
        })


@login_required

def cart_view(request):
    # Get the current user's cart items
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        total_amount = sum(cart.product.discounted_price * cart.quantity for cart in carts)
        amount = total_amount  # You can adjust this with discount logic if needed
        context = {
            'carts': carts,
            'total_amount': total_amount,
            'amount': amount,
        }
    else:
        carts = []
        context = {
            'carts': carts,
        }

    return render(request, 'product/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product is already in the cart
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.quantity += 1  # Increment quantity if product already exists in the cart
        cart_item.save()
    else:
        Cart.objects.create(user=user, product=product, quantity=1)

    messages.success(request, f'{product.name} has been added to your cart.')
    return redirect('cart_view')


@login_required
def remove_from_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    
    # Remove the product from the cart
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, f'{product.name} has been removed from your cart.')

    return redirect('cart_view')


@login_required
def clear_cart(request):
    user = request.user
    Cart.objects.filter(user=user).delete()
    messages.success(request, 'Your cart has been cleared.')

    return redirect('cart_view')
