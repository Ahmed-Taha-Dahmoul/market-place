from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Product, Order , Invoice
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import paypalrestsdk
from django.urls import reverse



# Your other views...

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order.html', {'order': order})


def checkout(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    }
    return render(request, 'checkout.html', context)

@csrf_exempt
def create_paypal_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    paypal_order = paypalrestsdk.Order({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment:order_success', args=[product.id])),
            "cancel_url": "http://127.0.0.1:8000/order/cancel/"
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
    })

    if paypal_order.create():
        payment_id = paypal_order.id  # Get the dynamically generated payment ID
        return JsonResponse({"order_id": payment_id})
    else:
        return JsonResponse({"error": paypal_order.error.message})



@csrf_exempt
def capture_paypal_order(request, order_id):
    paypal_payment = paypalrestsdk.Payment.find(order_id)

    if paypal_payment.execute({"payer_id": paypal_payment.payer.payer_info.payer_id}):
        # Payment captured successfully

        # Create a new Order instance for the successful payment
        try:
            product_id = paypal_payment.custom_id  # Get the product ID from the PayPal payment
            product = get_object_or_404(Product, pk=product_id)
            order = Order.objects.create(
                customer=request.user,  # Set the customer as the current user (assuming authentication is used)
                product=product,
                total_amount=float(paypal_payment.transactions[0].amount.total),
                payment_id=order_id,
                payment_status='good',
                status='created'
            )
            return JsonResponse({"message": "Payment captured successfully and order created.", "order_id": order.id})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."})
    else:
        return JsonResponse({"error": paypal_payment.error.message})



