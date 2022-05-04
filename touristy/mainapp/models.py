from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Search(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    search_str = models.CharField(max_length=100)
    class Meta:
        unique_together = ['user', 'search_str']

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)
    title = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    adress = models.CharField(max_length=60)
    class Meta:
        unique_together = ['latitude', 'longitude', 'title']

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=300)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['url', 'service']

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    stars = models.IntegerField()
    comment_str = models.CharField(max_length=200)
    class Meta:
        unique_together = ['user', 'service']
        constraints = [
            models.CheckConstraint(check=(models.Q(stars__gte=0) & models.Q(stars__lte=5)), name='stars_gte_0_lte_5'),
        ]

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    add_date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'service']

class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    class Meta:
        unique_together = ['title', 'user']

class Stop(models.Model):
    id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    stop_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    class Meta:
        unique_together = ['plan', 'service', 'stop_datetime']
