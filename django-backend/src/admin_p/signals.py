from asgiref.sync import async_to_sync
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from tables.models import TableModel
from channels.layers import get_channel_layer

@receiver(post_save, sender= TableModel)
def send_notification(sender, instance, created, **kwargs):
    if created:
        return
    channel_layer = get_channel_layer()
    group_name = 'notification-user'
    event = {
        'type': 'table_change',
        'text': instance.name
    }
    async_to_sync(channel_layer.group_send)(group_name, event)
