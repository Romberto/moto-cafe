from collections import OrderedDict
from unittest import TestCase

from category.models import Category
from product.models import Product
from product.serializers import ProductSerializers, ProductSerializerPost


class TestProductSerializer(TestCase):

    def setUp(self):
        self.category_1 = Category.objects.create(title="title_1")
        self.category_2 = Category.objects.create(title="title_2")

        self.product_1 = Product.objects.create(title='title_product_1', price=1000, photo_url="https://test.png",
                                                description="description_product_text", category=self.category_1)

        self.product_2 = Product.objects.create(title='title_product_2', price=2000, photo_url="https://test.png",
                                                description="description_product_text", category=self.category_1)

        self.product_3 = Product.objects.create(title='title_product_3', price=1500, photo_url="https://test.png",
                                                description="description_product_text", category=self.category_2)

    def test_api_product_serialiser(self):
        data = ProductSerializers([self.product_1, self.product_2, self.product_3], many=True).data
        expected_data = [
            OrderedDict(
                [('id', self.product_1.id), ('title', 'title_product_1'), ('price', '1000.00'), ('photo_url', 'https://test.png'),
                 ('description', 'description_product_text'), ('category', self.category_1.id), ('category_title', 'title_1')]),
            OrderedDict(
                [('id', self.product_2.id), ('title', 'title_product_2'), ('price', '2000.00'), ('photo_url', 'https://test.png'),
                 ('description', 'description_product_text'), ('category', self.category_1.id), ('category_title', 'title_1')]),
            OrderedDict(
                [('id', self.product_3.id), ('title', 'title_product_3'), ('price', '1500.00'), ('photo_url', 'https://test.png'),
                 ('description', 'description_product_text'), ('category', self.category_2.id), ('category_title', 'title_2')])
        ]

        self.assertEquals(expected_data, data)

    def test_serializer_post(self):
        category_2 = Category.objects.create(title="title_2")

        product_1 = Product.objects.create(title='title_product_1', price=1000, photo_url="https://test.png",
                                           description="description_product_text", category=category_2)

        product_2 = Product.objects.create(title='title_product_2', price=2000, photo_url="https://test.png",
                                           description="description_product_text", category=category_2)
        data = ProductSerializerPost([product_1, product_2], many=True).data
        expected_data = [
            {
                'id': product_1.id,
                'title': 'title_product_1',
                'price': '1000.00',
                'photo_url': 'https://test.png',
                'description': 'description_product_text',
                'category': category_2.id
            },
            {
                'id': product_2.id,
                'title': 'title_product_2',
                'price': '2000.00',
                'photo_url': 'https://test.png',
                'description': 'description_product_text',
                'category': category_2.id
            }
        ]
        self.assertEquals(data, expected_data)
