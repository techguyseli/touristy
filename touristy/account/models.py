from django.db import models
from django.contrib.auth.models import User

from service.models import Service

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='favorites')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='favorites')
    add_date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'service']

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='ratings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField()
    comment_str = models.CharField(max_length=200)
    class Meta:
        unique_together = ['user', 'service']
        constraints = [
            models.CheckConstraint(check=(models.Q(stars__gte=0) & models.Q(stars__lte=5)), name='stars_gte_0_lte_5'),
        ]

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='plans')
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    class Meta:
        unique_together = ['title', 'user']

class Stop(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='stops')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='stops')
    stop_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    class Meta:
        unique_together = ['plan', 'service', 'stop_datetime']