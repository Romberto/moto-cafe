from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse

from category.models import Category
from product.models import Product


class TestAdminPanel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password='1234erSDD')
        self.category_1 = Category.objects.create(title="title_1")
        self.category_2 = Category.objects.create(title="title_2")

        self.product_1 = Product.objects.create(title='title_product_1', price=1000, photo_url="https://test.png",
                                                description="description_product_text", category=self.category_1)

        self.product_2 = Product.objects.create(title='title_product_2', price=2000, photo_url="https://test.png",
                                                description="description_product_text", category=self.category_1)

        self.product_3 = Product.objects.create(title='title_product_3', price=1500, photo_url="https://test.png",
                                                description="description_product_text", category=self.category_2)

    def test_admin_panel_view_get_no_login(self):
        url = reverse('panel')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_admin_panel_view_get_login(self):
        url = reverse('panel')
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_p/AdminPanel.html')

    def test_admin_category_get_all_no_login(self):
        """
        test PanelCategoryView
        """
        url = reverse('panel_category')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_admin_category_get_all_login(self):
        url = reverse('panel_category')
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_p/AdminCategories.html')

    def test_admin_product_get_no_login(self):
        """
        test PanelProductView
        """
        url = reverse('panel_product')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_admin_product_get_login(self):
        url = reverse('panel_product')
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_p/AdminProducts.html')

    def test_admin_product_filter_no_login(self):
        """
        test PanelProductView filter
        """

        url = reverse('panel_product')
        data = {'category_title': 'title_1'}
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 302)

    def test_admin_product_filter_login(self):
        """
        test PanelProductView filter
        """

        url = reverse('panel_product')
        data = {'category_title': 'title_1'}
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)
        expected_data = [
            {'id': 1,
             'title': 'title_product_1',
             'category__title': 'title_1'},
            {'id': 2,
             'title': 'title_product_2',
             'category__title': 'title_1'}
        ]
        self.assertEquals(expected_data, response.context['object_list'])
        self.assertTemplateUsed('admin_p/AdminProducts.html')

    def test_product_detail_get_no_login(self):
        url = reverse('product_panel_detail', kwargs={'pk': self.product_1.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_product_detail_get_login(self):
        url = reverse('product_panel_detail', kwargs={'pk': self.product_1.id})
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('admin_p/AdminProductDetail.html')

    def test_product_detail_post_no_login(self):
        """
        test put product
        """
        url = reverse('product_panel_detail', kwargs={'pk': self.product_1.id})
        data = {
            "title": "title_54",
            'price': 2000,
            'photo_url': "https://test.trt",
            "description": "description",
            "category": self.category_1.id
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)

    def test_product_detail_post_login(self):
        """
        test put product
        """
        url = reverse('product_panel_detail', kwargs={'pk': self.product_1.id})
        data = {
            "title": "title_54",
            'price': 2000,
            'photo_url': "https://test.trt",
            "description": "description",
            "category": self.category_1.id
        }
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        self.product_1.refresh_from_db()
        self.assertEquals(self.product_1.title, 'title_54')

    def test_product_create_view_get_no_login(self):
        url = reverse('panel_product_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_product_create_view_get_login(self):
        url = reverse('panel_product_create')
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_p/AdminCreateProduct.html')

    def test_product_create_post_no_login(self):
        url = reverse('panel_product_create')
        data = {
            "title": "title_54",
            'price': 2000,
            'photo_url': "https://test.trt",
            "description": "description",
            "category": self.category_1.id
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)

    def test_product_create_post_login(self):
        url = reverse('panel_product_create')
        data = {
            "title": "title_54",
            'price': 2000,
            'photo_url': "https://test.trt",
            "description": "description",
            "category": self.category_1.id
        }
        beefore_data = Product.objects.count()
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        post_data = Product.objects.count()
        self.assertNotEquals(beefore_data, post_data)

    def test_category_create_get_no_login(self):
        url = reverse('panel_category_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_category_create_get_login(self):
        url = reverse('panel_category_create')
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_p/AdminCreateCategory.html')

    def test_category_create_post_no_login(self):
        url = reverse('panel_category_create')

        data = {
            'title': 'new_category'
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)

    def test_category_create_post_login(self):
        url = reverse('panel_category_create')
        count_beefore = Category.objects.count()
        data = {
            'title': 'new_category'
        }
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        count = Category.objects.count()
        self.assertNotEquals(count, count_beefore)

    def test_category_detail_view_get_no_login(self):
        """
        PanelCategoryDetailView get
        """
        url = reverse('panel_category_detail', kwargs={'pk': self.category_1.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_category_detail_view_get_login(self):
        """
        PanelCategoryDetailView get
        """
        url = reverse('panel_category_detail', kwargs={'pk': self.category_1.id})
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_p/AdminCategoryDetail.html')
        self.assertEquals(self.category_1, response.context['category'])
        self.assertEquals(2, len(response.context['products']))

    def test_category_detail_view_post_no_login(self):
        """
        PanelCategoryDetailView put
        """

        url = reverse('panel_category_detail', kwargs={'pk': self.category_1.id})
        data = {
            'title': 'title_54'
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)

    def test_category_detail_view_post_login(self):
        """
        PanelCategoryDetailView put
        """

        url = reverse('panel_category_detail', kwargs={'pk': self.category_1.id})
        data = {
            'title': 'title_54'
        }
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        self.category_1.refresh_from_db()
        self.assertEquals(self.category_1.title, 'title_54')

    def test_delete_product_no_login(self):
        url = reverse('product_delete', kwargs={'pk': self.product_1.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_delete_product_login(self):
        url = reverse('product_delete', kwargs={'pk': self.product_1.id})
        count_beefore = Product.objects.count()
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        count_now = Product.objects.count()
        self.assertNotEquals(count_now, count_beefore)

    def test_delete_category_no_login(self):
        url = reverse('category_delete', kwargs=({'pk': self.category_1.id}))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_delete_category_login(self):
        url = reverse('category_delete', kwargs=({'pk': self.category_1.id}))
        count_beefore = Category.objects.count()
        self.assertTrue(self.client.login(username='testuser1', password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        count_now = Category.objects.count()
        self.assertNotEquals(count_now, count_beefore)
