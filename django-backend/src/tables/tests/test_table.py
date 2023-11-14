from django.contrib.auth.models import User
from django.test import TestCase

from category.models import Category
from product.models import Product
from tables.views import form_menu_products


class TestTableMenu(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser_1", password="1234sde2")
        self.category_1 = Category.objects.create(title="title_1")
        self.category_2 = Category.objects.create(title="title_2")

        self.product_1 = Product.objects.create(title='title_product_1', price=1000,
                                                description="description_product_text", category=self.category_1)

        self.product_2 = Product.objects.create(title='title_product_2', price=2000,
                                                description="description_product_text", category=self.category_1)

        self.product_3 = Product.objects.create(title='title_product_3', price=1500,
                                                description="description_product_text", category=self.category_2)


    def test_get_menu(self):
        res = form_menu_products()
        expected_data ={'title_1': [self.product_2, self.product_1], 'title_2': [self.product_3]}
        self.assertEquals(res, expected_data)
