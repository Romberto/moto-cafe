from unittest import TestCase

from django.contrib.auth.models import User

from category.models import Category
from category.serializers import CategorySerializers


class TestCategorySerializer(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title="title_1")
        self.category2 = Category.objects.create(title="title_2")

    def test_categoryserializer(self):
        data = CategorySerializers([self.category1, self.category2], many=True).data
        expected_data = [
            {
                'id': self.category1.id,
                'title': 'title_1'
            },
            {
                'id': self.category2.id,
                'title': 'title_2'
            }
        ]
        self.assertEquals(expected_data, data)
