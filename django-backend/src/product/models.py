from django.db import models

from category.models import Category


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    photo_url = models.URLField(
        default="https://avatars.mds.yandex.net/i?id=7d5945d1f087f0300f467e9b4eac093999aa67d0-9853689-images-thumbs&n=13")
    description = models.CharField(max_length=255)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')

    def __str__(self):
        return f'id:{self.id} {self.title}'
