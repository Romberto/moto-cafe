# Generated by Django 4.2.6 on 2023-11-30 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_itemorders_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemorders',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders'),
        ),
    ]
