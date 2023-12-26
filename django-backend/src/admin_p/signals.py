from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from tables.models import TableModel


@receiver(post_save, sender=TableModel)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        # trigger notification to all consumers in the 'user-notification' group
        channel_layer = get_channel_layer()
        group_name = 'table-notification'
        event = {
            "type": "table_notification",
            "table_name": instance.name
        }
        async_to_sync(channel_layer.group_send)(group_name, event)