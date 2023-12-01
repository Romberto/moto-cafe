from django.test import TestCase

from django.contrib.auth.models import User, Group
from django.urls import reverse

from tables.models import TableModel
from waiter.forms import WaiterForm
from waiter.serializers import WaiterSerializer


class TestViewWaiter(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password='1234erSDD')
        self.user.first_name = 'Коля'
        self.user2 = User.objects.create_user(username="testuser2", password='1234erSDD')
        self.user_admin = User.objects.create_user(username="admin", password='1234erSDD')
        self.user_admin2 = User.objects.create_user(username="admin2", password='1234erSDD')
        self.my_group = Group.objects.create(name="Waiter")
        self.admins = Group.objects.create(name="Admins")
        self.my_group.user_set.add(self.user)
        self.my_group.user_set.add(self.user2)
        self.admins.user_set.add(self.user_admin)
        self.admins.user_set.add(self.user_admin2)
        self.table = TableModel.objects.create(name='teble_1', owner_officiant=self.user)


    def test_view_all_waiters_user_waiter(self):
        url = reverse('all_waiters')
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/panel/', status_code=302, target_status_code=200)

    def test_view_all_waiters_no_login(self):
        url = reverse('all_waiters')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_view_all_waiters(self):
        url = reverse('all_waiters')
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['object_list']), 2)
        expected = WaiterSerializer([self.user, self.user2], many=True)
        self.assertEquals(response.context['object_list'][0], self.user)
        self.assertEquals(response.context['object_list'][1], self.user2)

    def test_view_EditWaiter_no_login(self):
        url = reverse('edit_waiters', kwargs={'pk': self.admins.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_view_EditWaiter_no_admin(self):
        url = reverse('edit_waiters', kwargs={'pk': self.admins.id})
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/panel/', status_code=302, target_status_code=200)

    def test_view_EditWaiter(self):
        url = reverse('edit_waiters', kwargs={'pk': self.user.id})
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiter/WaiterEdit.html')
        self.assertEquals(response.context['waiter'], self.user)

    def test_post_EditWaiter_is_admin(self):
        url = reverse('edit_waiters', kwargs={'pk': self.user.id})
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.post(url, data={'first_name': 'Николай'})
        self.assertEquals(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, 'Николай')

    def test_delete_waiter_is_admin(self):
        url = reverse('delete_waiter', kwargs={'pk': self.user2.id})
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        expected = User.objects.filter(groups__name__in=['Waiter']).count() - 1
        response = self.client.post(url)
        self.assertRedirects(response, '/panel/', status_code=302, target_status_code=200)
        self.assertEquals(User.objects.filter(groups__name__in=['Waiter']).count(), expected)

    def test_delete_waiter_is_admin_protected(self):
        url = reverse('delete_waiter', kwargs={'pk': self.user.id})
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        expected = User.objects.filter(groups__name__in=['Waiter']).count()
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(User.objects.filter(groups__name__in=['Waiter']).count(), expected)

    def test_delete_waiter_is_waiter(self):
        url = reverse('delete_waiter', kwargs={'pk': self.user.id})
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.post(url)
        expected = User.objects.filter(groups__name__in=['Waiter']).count()
        self.assertRedirects(response, '/panel/', status_code=302, target_status_code=200)
        self.assertEquals(User.objects.filter(groups__name__in=['Waiter']).count(), expected)

    def test_delete_waiter_no_login(self):
        url = reverse('delete_waiter', kwargs={'pk': self.user.id})
        response = self.client.post(url)
        expected = User.objects.filter(groups__name__in=['Waiter']).count()
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)
        self.assertEquals(User.objects.filter(groups__name__in=['Waiter']).count(), expected)

    def test_CreateWaiter_no_login_get(self):
        url = reverse('add_waiter')
        response = self.client.get(url)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_CreateWaiter_is_waiter_get(self):
        url = reverse('add_waiter')
        self.assertTrue(self.client.login(username="testuser1", password='1234erSDD'))
        response = self.client.get(url)
        self.assertRedirects(response, '/panel/', status_code=302, target_status_code=200)

    def test_CreateWaiter_is_admin_get(self):
        url = reverse('add_waiter')
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiter/WaiterCreate.html')

    def test_CreateWaiter_no_login_post(self):
        url = reverse('add_waiter')
        data = {
            'username': "testuser3",
            'password1': '1234erSDD',
            'password2': '1234erSDD',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_CreateWaiter_is_waiter_post(self):
        url = reverse('add_waiter')
        data = {
            'username': "testuser3",
            'password1': '1234erSDD',
            'password2': '1234erSDD',
        }
        self.assertTrue(self.client.login(username="testuser2", password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertRedirects(response, '/panel/', status_code=302, target_status_code=200)

    def test_CreateWaiter_is_admin_post_no_valid(self):
        url = reverse('add_waiter')
        data = {
            'username': "testuser3",
            'password1': '1234erSD',
            'password2': '1234erSDD',
        }
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiter/WaiterCreate.html')


    def test_CreateWaiter_is_admin_post(self):
        url = reverse('add_waiter')
        data = {
            'username': "testuser3",
            'password1': '1234erSDD',
            'password2': '1234erSDD',
        }
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        expected = User.objects.filter(groups__name__in=['Waiter']).count() + 1
        response = self.client.post(url, data)
        self.assertRedirects(response, '/waiters/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertEquals(User.objects.filter(groups__name__in=['Waiter']).count(), expected)
        self.assertTrue(User.objects.get(username="testuser3"))
