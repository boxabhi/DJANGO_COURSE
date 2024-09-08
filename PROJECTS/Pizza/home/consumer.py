from channels.generic.websocket import WebsocketConsumer
import json
from .models import Pizza, Order
from asgiref.sync import async_to_sync, sync_to_async


class OrderProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        order = Order.give_order_details(self.room_name)
        self.accept()
        self.send(text_data=json.dumps({
            "payload" : order
        }))

    def order_status(self , event):
        data = json.loads(event['value'])

        self.send(text_data=json.dumps({
            'payload' : data
        }))
    
       
    def receive(self, text_data=None, bytes_data=None):
       pass



    def disconnect(self, close_code):
        pass