from decimal import Decimal

from django.test.testcases import TestCase

from django.urls import reverse

from category.models import Category
from product.models import Product


class TestCategoryView(TestCase):

    def setUp(self):
        self.category_1 = Category.objects.create(title="title_1")
        self.category_2 = Category.objects.create(title="title_2")

        self.product_1 = Product.objects.create(title='title_product_1', price=1000,
                                                description="description_product_text", category=self.category_1)

        self.product_2 = Product.objects.create(title='title_product_2', price=2000,
                                                description="description_product_text", category=self.category_1)

        self.product_3 = Product.objects.create(title='title_product_3', price=1500,
                                                description="description_product_text", category=self.category_2)

    def test_category_view_get(self):
        """
        test CategoryView
        """

        url = reverse('category')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/category_list.html')
        categories = Category.objects.all()
        self.assertEqual(len(categories), 2)  # Проверяем количество категорий
        self.assertEqual(categories[0], self.category_1)  # Проверяем, что категории в контексте правильно установлены
        self.assertEqual(categories[1], self.category_2)

