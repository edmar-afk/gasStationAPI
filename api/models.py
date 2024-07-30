from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_permit = models.FileField(
        upload_to='permits/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],
    )
    
    def __str__(self):
        return self.user.username


class GasStation(models.Model):
    station_name = models.ForeignKey(User, on_delete=models.CASCADE)
    gasoline_type = models.TextField()
    address = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    def __str__(self):
        return self.station_name

class Images(models.Model):
    station = models.ForeignKey(GasStation, on_delete=models.CASCADE)
    imges = models.FileField(
        upload_to='images/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],
    )


class ActivePromo(models.Model):
    station = models.ForeignKey(GasStation, on_delete=models.CASCADE)
    discount = models.IntegerField()
    expired_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.station