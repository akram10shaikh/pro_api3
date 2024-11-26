import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderStatusConsumer(AsyncWebsocketConsumer):
    user_sockets = {}
    vendor_sockets = {}

    async def connect(self):
        await self.accept()
        self.group_name = "order_status_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if hasattr(self, 'user_id') and self.user_id in self.user_sockets:
            self.user_sockets[self.user_id].remove(self)
            if not self.user_sockets[self.user_id]:
                del self.user_sockets[self.user_id]
        elif hasattr(self, 'restaurant_id') and self.restaurant_id in self.vendor_sockets:
            self.vendor_sockets[self.restaurant_id].remove(self)
            if not self.vendor_sockets[self.restaurant_id]:
                del self.vendor_sockets[self.restaurant_id]

    async def receive(self, text_data):
        data = json.loads(text_data)

        if 'userId' in data:
            self.user_id = data['userId']
            if self.user_id not in self.user_sockets:
                self.user_sockets[self.user_id] = []
            self.user_sockets[self.user_id].append(self)

        elif 'restaurantId' in data:
            self.restaurant_id = data['restaurantId']
            if self.restaurant_id not in self.vendor_sockets:
                self.vendor_sockets[self.restaurant_id] = []
            self.vendor_sockets[self.restaurant_id].append(self)

    async def updated(self, order):
        user_id = order['user']
        restaurant_id = order['restaurant']
        if user_id in self.user_sockets:
            for ws in self.user_sockets[user_id]:
                await ws.send(text_data=json.dumps(order))

        if restaurant_id in self.vendor_sockets:
            for ws in self.vendor_sockets[restaurant_id]:
                await ws.send(text_data=json.dumps(order))

    async def new(self, order):
        user_id = order['user']
        restaurant_id = order['restaurant']
        if user_id in self.user_sockets:
            for ws in self.user_sockets[user_id]:
                await ws.send(text_data=json.dumps(order))

        if restaurant_id in self.vendor_sockets:
            for ws in self.vendor_sockets[restaurant_id]:
                await ws.send(text_data=json.dumps(order))
    
