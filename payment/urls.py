from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    
    path('process_payment/<int:product_id>/<str:order_id>/', views.process_payment, name='process_payment'),
    
]
