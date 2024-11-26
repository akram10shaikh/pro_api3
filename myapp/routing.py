# myapp/routing.py
from django.urls import path
from myapp import consumers

websocket_urlpatterns = [
    path('ws/order/', consumers.OrderStatusConsumer.as_asgi()),
]
