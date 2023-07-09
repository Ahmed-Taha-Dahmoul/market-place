from django.urls import path
from . import views 
from home import views as home_views 
from django.conf.urls.static import static
from django.conf import settings
from payment import views as payment_views
app_name = 'seller' 

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('add_product/home1/',home_views.home1_view,name='home1' ),
    path('become_seller/', views.become_seller , name = 'become_seller'),
    path('buy/<int:product_id>/', payment_views.buy_product, name='buy_product'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)