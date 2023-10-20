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


class CategoryItemView(View):

    def get(self, request, pk):
        """
        все продукты одной категории
        """
        query_set = Product.objects.filter(category=pk).select_related('category').values('title', 'price', 'photo_url','description',
                                                                                          'category__title').order_by(
            'id')
        title = ''
        if query_set:
            title = query_set[0]['category__title']
        items_per_page = 10  # Количество объектов на странице
        paginator = Paginator(query_set, items_per_page)
        page = request.GET.get('page')  # Получение номера текущей страницы из параметра запроса
        try:
            current_page = paginator.page(page)
        except EmptyPage:
            current_page = paginator.page(1)  # Если номер страницы некорректный, отображаем первую страницу
        except PageNotAnInteger:
            current_page = paginator.page(1)
        return render(request, 'category/category_page.html', {'current_page': current_page, 'title': title})
