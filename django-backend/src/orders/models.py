from django.core.exceptions import ValidationError
from django.db import models

from tables.models import TableModel
from product.models import Product


class Orders(models.Model):

    STATUS = (("open", "счёт открыт"), ("check", "ожидает оплаты"), ("pay", "оплачен"))
    table_id = models.ForeignKey(TableModel, on_delete=models.PROTECT)
    status = models.CharField(max_length=12, choices=STATUS, default="open")

    def save(self, *args, **kwargs):
        # Проверяем, есть ли уже модель с таким table_id и статусами "счёт открыт" или "ожидает оплаты"
        existing_orders = Orders.objects.filter(table_id=self.table_id, status__in=["open", "check"])
        if existing_orders.exists():
            raise ValidationError("Модель с таким table_id и статусами 'счёт открыт' или 'ожидает оплаты' уже существует")
        super(Orders, self).save(*args, **kwargs)


    def __str__(self):
        return f"order-{self.id}: table{self.table_id.name}"


class ItemOrders(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.PROTECT)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f'item_order-{self.id}, prod - {self.product_id}'


