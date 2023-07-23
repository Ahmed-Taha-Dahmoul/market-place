from django.shortcuts import render, get_object_or_404
from django.conf import settings
from seller.models import Product , Seller_info , Customer
from .models import Order , Invoice
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

def create_paypal_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    paypal_api_url = "https://api.sandbox.paypal.com/v1/payments/payment"

    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET

    # Get the access token using OAuth 2.0 client credentials flow
    auth_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    data = {
        "grant_type": "client_credentials"
    }
    auth_response = requests.post(auth_url, auth=(client_id, client_secret), data=data, headers=headers)
    access_token = auth_response.json().get("access_token")

    if not access_token:
        return JsonResponse({"error": "Failed to obtain PayPal access token."})

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payload = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment:order_success', args=[product.id])),
            "cancel_url": reverse('payment:order_cancel')
        },
        "transactions": [
            {
                "amount": {
                    "total": str(product.product_price),
                    "currency": "USD"
                },
                "description": product.product_name
            }
        ]
    }

    response = requests.post(paypal_api_url, headers=headers, json=payload)

    if response.status_code == 201:
        # Extract the EC-XXX token from the PayPal API response
        ec_token = response.json()["links"][1]["href"].split("/")[-1]
        return JsonResponse({"order_id": ec_token})
    else:
        return JsonResponse({"error": "Failed to create PayPal order."})







from .models import Order  # Import the Order model at the top

# ... (previous code)

def order_success(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Your success message or additional processing logic here

    # Create an instance of the Order model
    order = Order.objects.create(
        customer=request.user,  # Assuming the authenticated user is the customer
        product=product,
        total_amount=product.product_price,
        payment_id=request.GET.get('paymentId', ''),  # Get the payment ID from the query parameters
        payment_status='success',  # Set the payment status to 'success' since it was successful
        # You may need to adjust this line depending on your use case for seller_info
        seller_info=product.seller_info,
        status = 'created'
    )

    order.save()

    return render(request, 'order_success.html', {'product': product})





def order_cancel(request):
    # Your cancelation logic here
    return render(request, 'order_cancel.html')
