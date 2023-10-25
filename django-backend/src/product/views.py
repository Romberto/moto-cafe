from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from product.models import Product
from product.serializers import ProductSerializers, ProductSerializerPost


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').only('id', 'title', 'price', 'description', 'photo',
                                                               'category', 'category__title')
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'category']
    search_fields = ['title', 'price']
    ordering_fields = ['title']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductSerializerPost  # Используйте другой сериализатор для метода POST
        return self.serializer_class
