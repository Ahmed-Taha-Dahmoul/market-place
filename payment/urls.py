from django.urls import path
from .views import coinbase_webhook

urlpatterns = [
    # Other URL patterns
    path('coinbase/webhook/', coinbase_webhook, name='coinbase_webhook'),
]