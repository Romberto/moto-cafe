from django.contrib import admin

from orders.models import Orders, ItemOrders


@admin.register(Orders)
class AdminOrders(admin.ModelAdmin):
    pass


@admin.register(ItemOrders)
class AdminItemOrders(admin.ModelAdmin):
    pass
