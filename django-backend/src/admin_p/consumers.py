from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template

class NotificationCunsumers(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.close()
            return
        self.GROUP_NAME = 'notification-user'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        self.accept()



    def disconnect(self, close_code):
        # Leave room group
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.GROUP_NAME, self.channel_name
            )

    def table_change(self, event):
        # html = get_template('admin_p/AdminPanel.html').render(
        #     context={
        #         'tablename': event['text']
        #     }
        # )
        self.send(text_data=(event['text']))