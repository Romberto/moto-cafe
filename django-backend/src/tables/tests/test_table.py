from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from category.models import Category
from orders.models import Orders, ItemOrders
from product.models import Product
from tables.models import TableModel
from tables.views import form_menu_products


class TestAjaxTable(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser_1", password="1234sde2")
        self.my_group = Group.objects.create(name="Waiter")
        self.my_group.user_set.add(self.user)
        self.user_admin = User.objects.create_user(username="admin", password='1234erSDD')
        self.admins = Group.objects.create(name="Admins")
        self.admins.user_set.add(self.user_admin)
        self.category_1 = Category.objects.create(title="title_1")
        self.product_1 = Product.objects.create(title='title_product_1', price=1000,
                                                description="description_product_text", category=self.category_1)

        self.table = TableModel.objects.create(name='1', owner_officiant=self.user)
        self.order = Orders.objects.create(table_id=self.table)
        self.item_order = ItemOrders.objects.create(order_id=self.order, product_id=self.product_1, count=3)

    def test_ajax_close_full_check(self):
        url = reverse('close_check')
        self.assertTrue(self.client.login(username="admin", password='1234erSDD'))
        data = {
            'table': self.table.name
        }
        response = self.client.post(url, data)
        self.table.refresh_from_db()
        self.assertEquals(self.table.owner_officiant,None)
        self.assertEquals(ItemOrders.objects.count(), 0)
        self.assertEquals(response.status_code, 200)

    def test_ajax_close_full_check_no_login(self):
        url = reverse('close_check')

        data = {
            'table': self.table.name
        }
        response = self.client.post(url, data)
        self.table.refresh_from_db()
        self.assertEquals(self.table.owner_officiant,self.user)
        self.order.refresh_from_db()
        self.assertEquals(self.order.status, 'open')
        self.assertRedirects(response, expected_url="/", status_code=302, target_status_code=200)

    def test_ajax_close_full_check_is_waiters(self):
        url = reverse('close_check')
        self.assertTrue(self.client.login(username="testuser_1", password="1234sde2"))
        data = {
            'table': self.table.name
        }
        response = self.client.post(url, data)
        self.table.refresh_from_db()
        self.assertEquals(self.table.owner_officiant,self.user)
        self.order.refresh_from_db()
        self.assertEquals(self.order.status, 'open')
        self.assertRedirects(response, expected_url="/panel/", status_code=302, target_status_code=200)


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
