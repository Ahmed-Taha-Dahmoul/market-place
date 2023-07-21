from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('order_success/<str:order_id>/', views.order_success, name='order_success'),
    path('capture_order/<str:order_id>/', views.capture_paypal_order, name='capture_paypal_order'),
]
