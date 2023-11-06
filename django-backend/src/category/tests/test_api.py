from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from category.models import Category
from category.serializers import CategorySerializers


class TestCategoryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password="12er43deAS")
        self.category1 = Category.objects.create(title="title_1")
        self.category2 = Category.objects.create(title="title_2")

    def test_category_api_get_all(self):
        url = reverse('category-list')
        self.assertTrue(self.client.login(username="testuser1", password="12er43deAS"))
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        expected_data = CategorySerializers([self.category1, self.category2], many=True)
        self.assertEquals(response.data, expected_data.data)
        count = Category.objects.count()
        self.assertEquals(count, 2)

    def test_api_get_one_category(self):
        url = reverse('category-detail', kwargs={"pk": self.category1.id})
        self.assertTrue(self.client.login(username="testuser1", password="12er43deAS"))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_data = CategorySerializers(self.category1).data
        self.assertEquals(expected_data, response.data)

    def test_api_post_create_category_no_login(self):
        url = reverse('category-list')
        data = {'title': "title_3"}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        count = Category.objects.count()
        self.assertEquals(count, 2)

    def test_api_post_create_category_login(self):
        url = reverse('category-list')
        data = {'title': "title_3"}
        self.assertTrue(self.client.login(username="testuser1", password="12er43deAS"))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        count = Category.objects.count()
        self.assertEquals(count, 3)

    def test_api_put_category_no_login(self):
        url = reverse('category-detail', kwargs={"pk": self.category1.id})
        data = {'title': 'new_tile'}
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        obj = Category.objects.get(id=self.category1.id)
        self.assertNotEquals(obj.title, "new_tile")

    def test_api_put_category_login(self):
        url = reverse('category-detail', kwargs={"pk": self.category1.id})
        data = {'title': 'new_tile'}
        self.assertTrue(self.client.login(username="testuser1", password="12er43deAS"))
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        obj = Category.objects.get(id=self.category1.id)
        self.assertEquals(obj.title, "new_tile")
