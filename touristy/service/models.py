from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='services')
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)
    title = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    adress = models.CharField(max_length=60)
    class Meta:
        unique_together = ['latitude', 'longitude', 'title']

class Image(models.Model):
    url = models.CharField(max_length=300)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    class Meta:
        unique_together = ['url', 'service']