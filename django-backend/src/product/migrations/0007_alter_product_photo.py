# Generated by Django 4.2.6 on 2023-10-23 10:32

from django.db import migrations
import django_resized.forms
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 300], upload_to=product.models.content_file_name),
        ),
    ]