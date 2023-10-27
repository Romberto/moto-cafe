from collections import OrderedDict
from io import BytesIO
from unittest import TestCase

from PIL import Image
from category.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile
from product.models import Product
from product.serializers import ProductSerializers, ProductSerializerPost


class TestProductSerializer(TestCase):

    def setUp(self):
        self.category_1 = Category.objects.create(title="title_1")
        self.category_2 = Category.objects.create(title="title_2")

        self.product_1 = Product.objects.create(title='title_product_1', price=1000,
                                                description="description_product_text", category=self.category_1)

        self.product_2 = Product.objects.create(title='title_product_2', price=2000,
                                                description="description_product_text", category=self.category_1)

        self.product_3 = Product.objects.create(title='title_product_3', price=1500,
                                                description="description_product_text", category=self.category_2)

    def test_api_product_serialiser(self):
        data = ProductSerializers([self.product_1, self.product_2, self.product_3], many=True).data
        expected_data = [
            OrderedDict([
                ('id', self.product_1.id),
                ('title',
                 'title_product_1'),
                ('price', '1000.00'),
                ('photo', '/media/default/no-photo-min.jpg'),
                ('description', 'description_product_text'),
                ('category', self.category_1.id),
                ('times', 10),
                ('category_title', 'title_1')]),
            OrderedDict([('id', self.product_2.id),
                         ('title', 'title_product_2'),
                         ('price', '2000.00'),
                         ('photo', '/media/default/no-photo-min.jpg'),
                         ('description', 'description_product_text'),
                         ('category', self.category_1.id),
                         ('times', 10),
                         ('category_title', 'title_1')]),
            OrderedDict([('id', self.product_3.id),
                         ('title', 'title_product_3'),
                         ('price', '1500.00'),
                         ('photo', '/media/default/no-photo-min.jpg'),
                         ('description', 'description_product_text'),
                         ('category', self.category_2.id),
                         ('times', 10),
                         ('category_title', 'title_2')])]

        self.assertEquals(expected_data, data)

    def test_serializer_post(self):
        data = ProductSerializerPost([self.product_1, self.product_2], many=True).data
        expected_data = [
            OrderedDict([('id', self.product_1.id),
                         ('title', 'title_product_1'),
                         ('price', '1000.00'),
                         ('photo', '/media/default/no-photo-min.jpg'),
                         ('description', 'description_product_text'),
                         ('times', 10),
                         ('category', self.category_1.id)]),
            OrderedDict([('id', self.product_2.id),
                         ('title', 'title_product_2'),
                         ('price', '2000.00'),
                         ('photo', '/media/default/no-photo-min.jpg'),
                         ('description', 'description_product_text'),
                         ('times', 10),
                         ('category', self.category_1.id)])
        ]

        self.assertEquals(data[0], expected_data[0])
