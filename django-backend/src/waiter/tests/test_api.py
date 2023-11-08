from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from waiter.serializers import WaiterSerializer


class TestWaiterViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password='1234erSDD')
        self.user2 = User.objects.create_user(username="testuser2", password='1234erSDD')
        self.user_admin = User.objects.create_user(username="admin", password='1234erSDD')
        self.user_admin2 = User.objects.create_user(username="admin2", password='1234erSDD')
        self.my_group = Group.objects.create(name="Waiter")
        self.admins = Group.objects.create(name="Admins")
        self.my_group.user_set.add(self.user)
        self.my_group.user_set.add(self.user2)
        self.admins.user_set.add(self.user_admin)
        self.admins.user_set.add(self.user_admin2)

    #  test get all
    def test_waiter_all_no_login(self):
        url = reverse('waiter-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_waiter_all_login(self):  # test get all
        url = reverse('waiter-list')
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_data = WaiterSerializer([self.user, self.user2], many=True)
        self.assertEquals(expected_data.data, response.data)

    def test_get_api_waiter_detail_no_login(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_api_waiter_detail_login(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        expected_data = WaiterSerializer(self.user)
        self.assertEquals(expected_data.data, response.data)

    # test post
    def test_post_api_waiter_no_login(self):
        url = reverse('waiter-list')
        data = {
            'username': "new_testuser",
            'password': '1234erSDD',
            'first_name': 'Tolic'
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_api_waiter_login_no_admin(self):
        url = reverse('waiter-list')
        data = {
            'username': "new_testuser",
            'password': '1234erSDD',
            'first_name': 'Tolic'
        }
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_api_waiter_login_admin(self):
        url = reverse('waiter-list')
        data = {
            'username': "new_testuser",
            'password': '1234erSDD',
            'first_name': 'Tolic'
        }
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.get(username="new_testuser")
        created_user.refresh_from_db()
        self.assertEquals(User.objects.filter(groups__name='Waiter').count(), 3)

    # test put

    def test_api_put_waiter_no_login(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        data = {
            'last_name': "new_last_name"
        }
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_put_waiter_login_no_admin(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        data = {
            'last_name': "new_last_name"
        }
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_put_login_admin(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        data = {
            'last_name': "new_last_name"
        }
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEquals(self.user.last_name, 'new_last_name')
        self.assertEquals(response.data['last_name'], 'new_last_name')

    # delete test

    def test_api_delete_waiter_no_login(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_waiter_login_no_admin(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_waiter_login_admin(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user.id})
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(User.objects.filter(groups__name='Waiter').count(), 1)

    def test_api_delete_no_waiter(self):
        url = reverse('waiter-detail', kwargs={'pk': self.user_admin2.id})
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(User.objects.filter(groups__name='Waiter').count(), 2)