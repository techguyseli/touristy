from django.db import models
# Create your models here.
'''
create table user(
    user_id int primary key auto_increment,
    user_name varchar(50) unique not null,
    user_hash varchar(200) not null,
    user_salt varchar(200) not null,
    status varchar(15) default 'active',
    history_on tinyint(1) default 0,
    constraint check_status check(status = 'active' or status = 'banned' or status = 'suspended'),
    constraint check_history_on check(history_on = 0 or history_on = 1)
);
'''
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=50,unique=True,null=False)
    user_hash = models.CharField(max_length=200,null=False)
    user_salt = models.CharField(max_length=200,null=False)
    status = models.CharField(max_length=15,null=False,default='active')
    history_on = models.models.PositiveSmallIntegerField(maxval=1,default=0)
    
'''
create table search(
    user_id int not null,
    search_str varchar(100) not null,
    constraint search_fk foreign key (user_id) references user(user_id) on delete cascade,
    unique search_unique (user_id, search_str)
);
'''
class search(models.Model):
    user = models.ForeignKey(User,unique=True,default=None)
    search_str = models.CharField(max_length=100,unique=True,null=False)

'''
create table admin(
    admin_id int primary key auto_increment,
    admin_name varchar(50) unique not null,
    admin_hash varchar(200) not null,
    admin_salt varchar(200) not null
);
'''
class admin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    admin_name = models.CharField(max_length=50,unique=True,null=False)
    admin_hash = models.CharField(max_length=200,null=False)
    admin_salt = models.CharField(max_length=200,null=False)

'''
create table service(
    service_id int primary key auto_increment,
    owner_id int not null,
    latitude double(20, 17) not null,
    longitude double(20, 17) not null,
    service_title varchar(40) not null,
    type varchar(20) not null,
    adress varchar(60) not null,
    constraint foreign key (owner_id) references user(user_id),
    unique service_composite_unique(latitude, longitude, service_title)
);
'''
class service(models.Model):
    service_id = models.IntegerField(primary_key=True)
    owner_id = models.ForeignKey(User,default=None)
    latitude = models.DoubleField(null=False,max_digits=20,decimal_places=17)
    longitude = models.DoubleField(null=False,max_digits=20,decimal_places=17)
    service_title = models.CharField(max_length=40,null=False)
    type = models.CharField(max_length=20,null=False)
    adress = models.CharField(max_length=60,null=False)


