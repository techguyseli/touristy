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