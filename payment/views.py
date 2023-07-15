from django.shortcuts import render, redirect
from coinbase_commerce.client import Client
from seller.models import Product, Picture
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from coinbase_commerce.webhook import Webhook
from coinbase_commerce.error import WebhookInvalidPayload, SignatureVerificationError
from .models import Order
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone

client = Client(api_key='b39fe826-e6a0-4268-8d0c-6367a7885042')

def buy_product(request, product_id):
    # Get the product details and perform the buy action
    product = Product.objects.get(pk=product_id)

    if product.product_price == 0:
        local_price = {'amount': str(Decimal('0.01')), 'currency': 'USD'}
    else:
        local_price = {'amount': str(Decimal(product.product_price)), 'currency': 'USD'}

    # Create a charge
    charge = client.charge.create(
        name=product.product_name,
        description=product.product_description,
        local_price=local_price,
        pricing_type='fixed_price',
        metadata={'product_id': product_id},
    )

    # Perform any necessary actions (e.g., update database, send email notifications, etc.)

    # Redirect the user to the Coinbase Commerce checkout URL
    return redirect(charge['hosted_url'])

@csrf_exempt
def coinbase_webhook(request):
    # Verify the authenticity of the webhook request
    try:
        payload = request.body.decode('utf-8')
        signature = request.headers.get('X-CC-Webhook-Signature')
        Webhook.verify_signature(payload, signature, 'your_webhook_secret')
    except (WebhookInvalidPayload, SignatureVerificationError):
        # Handle verification failure (e.g., log the error, return an error response)
        return HttpResponse(status=400)

    # Process the webhook event
    event = Webhook.construct_event(payload, signature)
    if event.type == 'charge:confirmed':
        # Payment is confirmed, update the purchase status in your system
        charge_id = event.data['id']
        # Retrieve the corresponding purchase from your database using the charge ID
        # Update the purchase status to 'completed' or perform any other necessary actions
        
        # Create an order for the confirmed payment
        product_id = event.data['metadata']['product_id']
        product = Product.objects.get(pk=product_id)
        customer = User.objects.get(username=event.data['metadata']['customer_username'])
        total_amount = float(event.data['pricing']['local']['amount'])
        order = Order.objects.create(customer=customer, product=product, total_amount=total_amount, order_date=timezone.now(), status='created')
        
        # Perform any other actions you need for the order
        
    # Return a success response to Coinbase
    return HttpResponse(status=200)

def order_view(request, charge_id):
    # Retrieve the order details from the charge ID
    try:
        order = Order.objects.get(charge_id=charge_id)
        context = {
            'order': order,
            'seller_info': order.seller_info  # Include seller's information in the context
        }
        return render(request, 'order.html', context)
    except Order.DoesNotExist:
        return HttpResponse("Order not found")
