from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db.models.signals import post_save



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the instance is being created for the first time
        super().save(*args, **kwargs)
        if created:
            # Create a corresponding Seller_info instance for the newly created Customer
            Seller_info.objects.create(customer=self.user, first_name='', second_name='', documents='', description='', verified=False)

    


class Seller_info(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    documents = models.FileField(upload_to='seller_documents')
    description = models.TextField()
    verified = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)


    def __str__(self):
        return str(self.customer.username)



class Product(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=500)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller_info = models.ForeignKey(Seller_info, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.product_name




class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.image.name

@receiver(pre_delete, sender=Picture)
def delete_picture_files(sender, instance, **kwargs):
    # Delete the image file from storage when the picture is deleted
    if instance.image:
        default_storage.delete(instance.image.path)