from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from category.models import Category
from product.models import Product
from product.serializers import ProductSerializers


class TestProductViewSet(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser_1", password="1234sde2")
        self.category_1 = Category.objects.create(title="title_1")
        self.category_2 = Category.objects.create(title="title_2")

        self.product_1 = Product.objects.create(title='title_product_1', price=1000, photo_url="https://test.png",
                                           description="description_product_text", category=self.category_1)

        self.product_2 = Product.objects.create(title='title_product_2', price=2000, photo_url="https://test.png",
                                           description="description_product_text", category=self.category_1)

        self.product_3 = Product.objects.create(title='title_product_3', price=1500, photo_url="https://test.png",
                                           description="description_product_text", category=self.category_2)

    def test_api_get_all_product(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = ProductSerializers([self.product_1, self.product_2, self.product_3], many=True).data
        self.assertEquals(data, response.data)
        count = Product.objects.count()
        self.assertEquals(count, 3)

    def test_api_create_product_no_login(self):
        category_1 = Category.objects.create(title="title_1")
        url = reverse('product-list')

        data = {
            'title': "test_title",
            'price': 1000,
            'photo_url': "https://rrrtest.tr",
            'description': "test_description",
            'category': category_1.id
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        count = Product.objects.count()
        self.assertEquals(count, 3)


    def test_api_create_product_login(self):
        category_1 = Category.objects.create(title="title_1")
        url = reverse('product-list')

        data = {
            'title': "test_title",
            'price': 1000,
            'photo_url': "https://rrrtest.tr",
            'description': "test_description",
            'category': category_1.id
        }
        self.assertTrue(self.client.login(username='testuser_1', password='1234sde2'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        count = Product.objects.count()
        self.assertEquals(count, 4)

