from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import WebsocketConsumer


class Notification(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = 'table-notification'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME,
            self.channel_name
        )
        self.accept()
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )

    def table_notification(self, event):

        self.send(text_data=event['table_name'])