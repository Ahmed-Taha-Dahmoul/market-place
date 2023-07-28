from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from seller.models import Product , Seller_info , Customer
from .models import Order
from django.urls import reverse
import paypalrestsdk
from django.middleware.csrf import get_token
import requests
from django.http import JsonResponse

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def checkout(request, product_id):
    
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'product_id': product_id,  # Add the product_id to the context
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
        'csrf_token': get_token(request),
    }
    return render(request, 'checkout.html', context)


import requests
from django.http import JsonResponse

# ... (previous code)



# ... (previous code)

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Order
from seller.models import Product

# ... (previous code)

from django.http import HttpResponseServerError

def process_payment(request, product_id, order_id):
    # Get the payment status from the query parameters
    payment_status = request.GET.get('payment_status')

    # Check if the payment is successful (you might need to implement additional checks based on PayPal's response)
    if payment_status == 'success':
        # Check if an order with the given order_id already exists
        existing_order = Order.objects.filter(payment_id=order_id).first()
        if existing_order:
            # If an order with this order_id already exists, render the success page and return
            context = {
                'order': existing_order
            }
            return render(request, 'payment_success.html', context)
        
        # Get the product associated with the PayPal order (you might need additional checks)
        product = get_object_or_404(Product, pk=product_id)
        # Create a new Order instance for the successful payment
        order = Order.objects.create(
            customer=request.user,
            product=product,
            total_amount=product.product_price,
            payment_id=order_id,
            payment_status='success',
            status='created'  # Set any initial status you prefer
        )

        # Your additional processing logic here, if needed
        # For example, you can update the status of the product to 'sold' or perform any other actions

        # Save the order instance
        order.save()
        context = {
            'order': order,
            'product':product
        }

        # Redirect to a success page or display a success message
        return render(request, 'payment_success.html', context)
    else:
        # Handle unsuccessful payments (optional: you can redirect to a cancel page or display an error message)
        return render(request, 'order_cancel.html')


