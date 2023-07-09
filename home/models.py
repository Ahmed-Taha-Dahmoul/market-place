from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    

    # Add any other fields and methods as needed

    def __str__(self):
        return self.user.username
# Create your models here.
