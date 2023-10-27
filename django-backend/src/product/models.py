from django.db import models
from django_resized import ResizedImageField
from category.models import Category


def content_file_name(instance, filename):
    return '/'.join(['products', str(instance.category.id), filename])


class Product(models.Model):
    title = models.CharField(max_length=200)  # название блюда
    price = models.DecimalField(max_digits=7, decimal_places=2)  # цена
    description = models.CharField(max_length=150)  # состав или описание продукта
    times = models.IntegerField(default=10)  # время приготовления
    photo = ResizedImageField(size=[500, 300], upload_to=content_file_name, null=True, blank=True,
                              default='default/no-photo-min.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')

    def __str__(self):
        return f'id:{self.id} {self.title}'
