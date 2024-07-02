from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth import get_user_model
from .models import Conversation, Message
import logging
from pprint import pformat
from asgiref.sync import async_to_sync

logger = logging.getLogger('django')

User=get_user_model()
class WebChatConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None

    def connect(self):
        self.user=self.scope['user']
        print(self.user)
        if not self.user.is_authenticated:
            self.close(code=4001)
            return
        self.accept()
        if self.scope is None:
            print("ye toh kuch nhi")
        self.channel_id = self.scope['url_route']['kwargs']['channelId']
        async_to_sync(self.channel_layer.group_add)(self.channel_id,self.channel_name)
        

    def receive_json(self, content):
        channel_id = self.channel_id
        sender = self.user
        message = content["message"]

        conv, _ = Conversation.objects.get_or_create(channel_id=channel_id)
        new_message = Message.objects.create(conversation=conv, sender=sender, content=message)
        new_message.save()

        async_to_sync(self.channel_layer.group_send)(self.channel_id, {
            "type": "chat.message",
            "id": new_message.id,
            "sender": sender.get_username(),
            "content": new_message.content,
            'timestamp': new_message.timestamp.isoformat()
        })
        print(f"Message sent to group: {self.channel_id}")


    def chat_message(self, event):
        self.send_json(event)
 
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.channel_id, self.channel_name)
        super().disconnect(close_code)
