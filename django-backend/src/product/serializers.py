from rest_framework.serializers import ModelSerializer, CharField

from product.models import Product


class ProductSerializers(ModelSerializer):
    category_title = CharField(source="category.title", max_length=100)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'photo', 'description', 'category', 'times','category_title')


class ProductSerializerPost(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'photo', 'description', 'times', 'category')
