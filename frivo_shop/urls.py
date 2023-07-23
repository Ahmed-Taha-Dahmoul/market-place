from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('seller/', include('seller.urls')),
    path('payment/', include('payment.urls')),
    path('conversation/', include('conversation.urls')),
]
