from django.contrib import admin
from myapp.models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(RestaurantName)
admin.site.register(Order)
admin.site.register(Ticket_raise)
admin.site.register(Subscription)
admin.site.register(Feedback)
admin.site.register(FCMDevice)
