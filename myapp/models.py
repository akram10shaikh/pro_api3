from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('male', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=30,null=True,choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=100,null=True)
    profile_image = models.CharField(max_length=500,null=True)
    is_active = models.BooleanField(default=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # qr_code = models.CharField(max_length=500)



    @receiver(post_save,sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class RestaurantName(models.Model):
    user = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    restaurant_name = models.CharField(max_length=70,null=True)
    address_line1 = models.CharField(max_length=255,null=True)
    address_line2 = models.CharField(max_length=255,null=True)
    pin_code = models.IntegerField(null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    restaurant_image = models.CharField(max_length=500,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    verify = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    labels = models.JSONField(default=list, null=True, blank=True)
    resturantoff = models.DateField(null=True)


    def __str__(self):
        return self.restaurant_name

class Order(models.Model):
    user = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE)
    resturant = models.ForeignKey(RestaurantName,on_delete=models.CASCADE,null=True)
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    image = models.CharField(max_length=255,null=True)
    bill_id = models.IntegerField(null=True)
    order_date = models.DateTimeField(null=True , default=timezone.now)
    delivery_data = models.CharField(max_length=255,null=True)
    amount = models.IntegerField(null=True)
    note = models.CharField(max_length=255,null=True)

    tag = models.JSONField(default=list,null=True,blank=True)
    ORDER_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('order ready', 'Order ready'),
        ('completed', 'Completed'),
    ]
    order_status = models.CharField(max_length=255,null=True,choices=ORDER_CHOICES)

    def __str__(self):
        return self.customer_name


class Ticket_raise(models.Model):
    user = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE)
    resturant = models.ForeignKey(RestaurantName,on_delete=models.CASCADE,null=True)
    select_order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    email = models.EmailField(max_length=255,null=True)
    # select_order = models.CharField(max_length=255,null=True)
    attach_file = models.CharField(max_length=500,null=True)
    description = models.TextField(null=True)
    date_time = models.DateTimeField(auto_now_add=True,null=True)
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=100,null=True,choices=STATUS_CHOICES)

    def __str__(self):
        return self.email

class Feedback(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    about = models.CharField(max_length=400,null=True)
    issue = models.CharField(max_length=400,null=True)
    message = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE)
    active = models.CharField(null=True,max_length=200)

    def __str__(self):
        return self.user.username

class FCMDevice(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    device = models.CharField(max_length=300,null=True)
    platform = models.CharField(max_length=300,null=True)
    active = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=300,null=True)








