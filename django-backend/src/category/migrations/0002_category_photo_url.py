# Generated by Django 4.2.6 on 2023-10-10 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
