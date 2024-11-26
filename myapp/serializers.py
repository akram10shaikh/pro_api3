# serializers.py
from rest_framework import serializers
from .models import *

class MyCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class MyRestaurantNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantName
        fields = '__all__'


class MyOrderSerializer(serializers.ModelSerializer):
    resturant_data = MyRestaurantNameSerializer(source='resturant', read_only=True)
    class Meta:
        model = Order
        fields = ["id","customer_name","address","image","bill_id","order_date","delivery_data","amount","note","tag","order_status","user","resturant_data"]


class MyTicket_raiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_raise
        fields = '__all__'

class MyFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SingleVariableSerializer(serializers.Serializer):
    token = serializers.CharField()


class MySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = '__all__'

