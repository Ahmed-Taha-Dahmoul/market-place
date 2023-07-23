from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('create_paypal_order/<int:product_id>/', views.create_paypal_order, name='create_paypal_order'),
    path('order_success/<int:product_id>/', views.order_success, name='order_success'),
    path('order_cancel/', views.order_cancel, name='order_cancel'),
]
