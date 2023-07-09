import logging
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Customer, Product, Picture, Seller_info
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (CustomerInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            # If it's a new User, create a corresponding Customer instance
            Customer.objects.create(user=obj)


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('user',)
    # Add any other customizations for the Customer admin


class SellerInfoAdmin(admin.ModelAdmin):
    model = Seller_info
    list_display = ('customer', 'verified')
    # Add any other customizations for the Seller_info admin


@receiver(post_save, sender=Seller_info)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        logger = logging.getLogger(__name__)
        logger.info('New Seller_info application submitted. Customer: %s, Verified: %s', instance.customer, instance.verified)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)
admin.site.register(Picture)
admin.site.register(Seller_info, SellerInfoAdmin)
