from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from seller import views as sl

urlpatterns = [
    
    path('', views.home_page, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home1/', views.home1_view, name='home1'),
    path('product_detail/<int:product_id>/', sl.product_detail, name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)