from django.shortcuts import render,get_object_or_404,redirect
from product.models import Product,Cart
from django.views import View
from decimal import Decimal 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.

def Home(request):
    return render(request,'base.html')

# def VegFruit(request):
#     products = Product.objects.all()
#     return render(request,'product/vege_fruit.html',{'products': products})



from django.shortcuts import render
from django.db.models import Q

# View for Vegetable & Fruits category
def VegFruit(request):
    # Base queryset for "Vegetable & Fruits" category
    products = Product.objects.filter(category="Vegetable & Fruits")

    # Get filtering parameters from the request
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort_by', '')

    # Apply search filter
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Apply sorting logic
    if sort_by == 'low_to_high':
        products = products.order_by('selling_price')  # Ascending price
    elif sort_by == 'high_to_low':
        products = products.order_by('-selling_price')  # Descending price
    else:
        products = products.order_by('-id')  # Default: newest first

    # Context for rendering the template
    context = {
        'products': products,
        'query': query,
        'selected_sort': sort_by,
    }

    return render(request, 'product/vege_fruit.html', context)


# def GrainOil(request):
#     products = Product.objects.all()
#     return render(request,'product/grain_oil.html',{'products': products})




from django.shortcuts import render
from django.db.models import Q

# View for Vegetable & Fruits category
def GrainOil(request):
    # Base queryset for "Vegetable & Fruits" category
    products = Product.objects.filter(category="FoodGrains & Oil")

    # Get filtering parameters from the request
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort_by', '')

    # Apply search filter
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Apply sorting logic
    if sort_by == 'low_to_high':
        products = products.order_by('selling_price')  # Ascending price
    elif sort_by == 'high_to_low':
        products = products.order_by('-selling_price')  # Descending price
    else:
        products = products.order_by('-id')  # Default: newest first

    # Context for rendering the template
    context = {
        'products': products,
        'query': query,
        'selected_sort': sort_by,
    }

    return render(request, 'product/grain_oil.html', context)


def Shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request,'product/shop.html',context)

def DairyProduct(request):
    # Base queryset for "Vegetable & Fruits" category
    products = Product.objects.filter(category="DairyProducts")

    # Get filtering parameters from the request
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort_by', '')

    # Apply search filter
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Apply sorting logic
    if sort_by == 'low_to_high':
        products = products.order_by('selling_price')  # Ascending price
    elif sort_by == 'high_to_low':
        products = products.order_by('-selling_price')  # Descending price
    else:
        products = products.order_by('-id')  # Default: newest first

    # Context for rendering the template
    context = {
        'products': products,
        'query': query,
        'selected_sort': sort_by,
    }

    return render(request, 'product/dairyproduct.html', context)

def ContactUs(request):
    return render(request,'product/contact.html')
# def Home(request):
#     products = Product.objects.filter(category="Gallery")
#     brands = products.values_list('brand', flat=True).distinct()
#     brand = request.GET.get('brand')
#     if brand and brand != 'All':
#         products = products.filter(brand=brand)
#     sort_by = request.GET.get('sort_by')
#     if sort_by == 'low_to_high':
#         products = products.order_by('selling_price')
#     elif sort_by == 'high_to_low':
#         products = products.order_by('-selling_price')
#     context = {
#         'products': products,
#         'brands': brands,
#         'selected_brand': brand,
#         'selected_sort': sort_by,
#     }
#     return render(request, 'product/clothesGallery.html', context)


class ProductDetail(View):
    def get(self,request,pk):
        product = get_object_or_404(Product, pk=pk)             
        context = {
            'product': product,
            
        }
        return render (request,'product/detailPage.html',context)
    


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required

def AddCart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if product already exists in the cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        # Increase quantity if product is already in cart
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Product quantity updated in cart.")
    else:
        messages.success(request, "Product added to cart.")

    # Redirect to cart page
    return redirect('Show_Cart')


from django.db.models import Sum, F

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate the total amount and subtotal
    subtotal = cart_items.aggregate(total=Sum(F('quantity') * F('product__discounted_price')))['total'] or 0
    shipping = 50  # Fixed shipping cost
    total_amount = subtotal + shipping

    context = {
        'carts': cart_items,
        'amount': subtotal,
        'total_amount': total_amount,
    }

    return render(request, 'product/cart.html', context)





# def AddCart(request):
#      # Check if the user is authenticated
#     if not request.user.is_authenticated:
#         messages.error(request, "You need to log in first to add items to the cart.")
#         return redirect('Home')  # Replace 'login' with the name of your login URL pattern
    
#     user = request.user
#     product_id = request.GET.get('prod_id') 
#     try:
#         product = Product.objects.get(id=product_id)
        
#         # Check if the product is already in the cart
#         cart_item = Cart.objects.filter(user=user, product=product).first()
#         if cart_item:
#             messages.info(request, 'Selected product is already in cart')
#         else:
#             Cart(user=user, product=product).save()
#             messages.success(request, 'Product added to cart successfully!')
#     except Product.DoesNotExist:
#         pass

#     if request.user.is_authenticated:
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount = Decimal(0.0)  # Use Decimal for consistency
#         shipping_amount = Decimal(70.0)  # Convert shipping amount to Decimal
#         total_amount = Decimal(0.0)
#         cart_product = Cart.objects.filter(user=user)  # Filter by user directly in the query
        
#         if cart_product:
#             for p in cart_product:
#                 tempamount = (p.quantity * p.product.discounted_price)  # Assume discounted_price is Decimal
#                 amount += tempamount
#             total_amount = amount + shipping_amount
        
#         return render(request, 'product/cart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})


def ShowCart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = Decimal(0.0)  # Use Decimal for consistency
        shipping_amount = Decimal(70.0)  # Convert shipping amount to Decimal
        total_amount = Decimal(0.0)
        cart_product = Cart.objects.filter(user=user)  # Filter by user directly in the query
        
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)  # Assume discounted_price is Decimal
                amount += tempamount
            total_amount = amount + shipping_amount
        
        return render(request, 'product/cart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount})
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated
       

    
def update_cart_quantity(request, cart_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    action = request.POST.get('action')
    
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                messages.warning(request, 'Quantity cannot be less than 1')
                
        cart_item.save()
        messages.success(request, 'Cart updated successfully!')
        
    except Cart.DoesNotExist:
        messages.error(request, 'Cart item not found')
    
    return redirect('Show_Cart')

def remove_from_cart(request, cart_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        cart_item = Cart.objects.get(id=cart_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Product removed from cart successfully!')
        
    except Cart.DoesNotExist:
        messages.error(request, 'Cart item not found')
    
    return redirect('Show_Cart')

def calculate_cart_totals(user):
    cart_items = Cart.objects.filter(user=user)
    amount = Decimal('0.0')
    shipping_amount = Decimal('70.0')
    
    for item in cart_items:
        amount += item.quantity * item.product.discounted_price
    
    total_amount = amount + shipping_amount
    return amount, total_amount







