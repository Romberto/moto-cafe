from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from category.models import Category
from category.serializers import CategorySerializers

from product.models import Product


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryView(ListView):
    """
    все категории
    """
    model = Category


