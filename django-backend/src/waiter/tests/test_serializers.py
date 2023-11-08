from collections import OrderedDict

from django.contrib.auth.models import Group, User
from django.test import TestCase

from waiter.serializers import WaiterSerializer, WaiterCreateSerializer


class TestWaiterSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password='1234erSDD')
        self.user2 = User.objects.create_user(username="testuser2", password='1234erSDD')
        self.user_admin = User.objects.create_user(username="admin", password='1234erSDD')
        self.user_admin2 = User.objects.create_user(username="admin2", password='1234erSDD')
        self.my_group = Group.objects.create(name="Waiter")
        self.admins = Group.objects.create(name="Admins")
        self.user.groups.add(self.my_group)

        self.my_group.user_set.add(self.user2)
        self.admins.user_set.add(self.user_admin)
        self.admins.user_set.add(self.user_admin2)

    def test_WaiterSerializer(self):
        data = WaiterSerializer(self.user).data
        expected_data = {
            'id': self.user.id,
            'username': 'testuser1',
            'first_name': '',
            'last_name': '',
            'groups': [self.my_group.id]
        }
        self.assertEquals(data, expected_data)

    def test_WaiterSerializer_many(self):
        data = WaiterSerializer([self.user, self.user2],many=True).data
        expected_data = [OrderedDict([('id', self.user.id), ('username', 'testuser1'), ('first_name', ''), ('last_name', ''), ('groups', [self.my_group.id])]), OrderedDict([('id', self.user2.id), ('username', 'testuser2'), ('first_name', ''), ('last_name', ''), ('groups', [self.my_group.id])])]
        self.assertEquals(data, expected_data)

    def test_WaiterCreateSerializer(self):
        data = WaiterCreateSerializer(self.user).data
        expected_data = {'id': self.user.id, 'username': 'testuser1', 'password': self.user.password, 'first_name': '', 'last_name': ''}
        self.assertEquals(data, expected_data)