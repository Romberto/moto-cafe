from django.test.testcases import TestCase

from django.urls import reverse

from category.models import Category
from product.models import Product


class TestCategoryView(TestCase):

    def test_category_view_get(self):
        """
        test CategoryView
        """
        category_1 = Category.objects.create(title="title_1")
        category_2 = Category.objects.create(title="title_2")
        url = reverse('category')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/category_list.html')
        categories = Category.objects.all()
        self.assertEqual(len(categories), 2)  # Проверяем количество категорий
        self.assertEqual(categories[0], category_1)  # Проверяем, что категории в контексте правильно установлены
        self.assertEqual(categories[1], category_2)

    def test_category_item_get(self):
        """
        test CategoryItemView
        """
        category_1 = Category.objects.create(title="title_1")
        category_2 = Category.objects.create(title="title_2")

        product_1 = Product.objects.create(title='title_product_1', price=1000, photo_url="https://test.png",
                                           description="description_product_text", category=category_1)

        product_2 = Product.objects.create(title='title_product_2', price=2000, photo_url="https://test.png",
                                           description="description_product_text", category=category_1)

        product_3 = Product.objects.create(title='title_product_3', price=1500, photo_url="https://test.png",
                                           description="description_product_text", category=category_2)
        url = reverse('category_item', kwargs={'pk': category_1.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/category_page.html')
        query_set = Product.objects.filter(category=category_1.id).select_related('category').values('title', 'price',
                                                                                                     'photo_url',
                                                                                                     'category__title').order_by(
            'id')
        self.assertEqual(len(query_set), 2)
        expected_product_1 = {
            'title': 'title_product_1',
            'price': 1000.00,
            'photo_url': 'https://test.png',
            'category__title': 'title_1'
        }
        self.assertEqual(query_set[0], expected_product_1)  # Проверяем, что категории в контексте правильно установлены
        expected_product_2 = {
            'title': 'title_product_2',
            'price': 2000.00,
            'photo_url': 'https://test.png',
            'category__title': 'title_1'
        }
        self.assertEqual(query_set[1], expected_product_2)
