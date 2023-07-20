from django.db import models
from seller.models import Product, Seller_info
from django.contrib.auth.models import User
from django.contrib import admin


class Invoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller_info = models.ForeignKey(Seller_info, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller_info = models.ForeignKey(Seller_info, on_delete=models.CASCADE, default=None)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    # Add any other fields relevant to an order
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('preparing', 'Preparing'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    def __str__(self):
        return f"Order #{self.pk} - {self.product.product_name}"


admin.site.register(Invoice)
admin.site.register(Order)
