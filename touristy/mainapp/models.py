from django.db import models
# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50,unique=True,null=False)
    user_hash = models.CharField(max_length=200,null=False)
    user_salt = models.CharField(max_length=200,null=False)
    status = models.CharField(max_length=15,null=False,default='active')
    history_on = models.models.PositiveSmallIntegerField(maxval=1,default=0)
    

class search(models.Model):
    search_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    search_str = models.CharField(max_length=100,unique=True,null=False)
    class Meta:
        unique_together = ['user_id', 'search_str']
    


class admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50,unique=True,null=False)
    admin_hash = models.CharField(max_length=200,null=False)
    admin_salt = models.CharField(max_length=200,null=False)


class service(models.Model):
    service_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User',default=None)
    latitude = models.DoubleField(null=False,max_digits=20,decimal_places=17)
    longitude = models.DoubleField(null=False,max_digits=20,decimal_places=17)
    service_title = models.CharField(max_length=40,null=False)
    type = models.CharField(max_length=20,null=False)
    adress = models.CharField(max_length=60,null=False)
    class Meta:
        unique_together = ['latitude', 'longitude', 'service_title']


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=300)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)
    class Meta:
        unique_together = ['image_url', 'service_id']


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)
    stars = models.IntegerField()
    comment_str = models.CharField(max_length=200)
    class Meta:
        unique_together = ['user_id', 'service_id']
        constraints = [
            models.CheckConstraint(check=(models.Q(stars__gte=0) & models.Q(stars__lte=5)), name='stars_gte_0_lte_5'),
        ]


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)
    add_date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ['user_id', 'service_id']


class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    plan_title = models.CharField(max_length=30)
    plan_description = models.CharField(max_length=100)
    plan_start = models.DateField(auto_now=False, auto_now_add=False)
    plan_end = models.DateField(auto_now=False, auto_now_add=False)
    class Meta:
        unique_together = ['plan_title', 'user_id']


class Stop(models.Model):
    stop_id = models.AutoField(primary_key=True)
    plan_id = models.ForeignKey('Plan', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE)
    stop_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    class Meta:
        unique_together = ['plan_id', 'service_id', 'stop_datetime']
