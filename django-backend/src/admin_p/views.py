from PIL import Image

import django_filters
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from admin_p.decorators import custom_login_required
from category.forms import CategoryForm
from category.models import Category
from product.forms import ProductForm
from product.models import Product


@method_decorator(login_required, name='dispatch')
class PanelView(View):
    def get(self, request):
        return render(request, 'admin_p/AdminPanel.html')


@method_decorator(login_required, name='dispatch')
class PanelCategoryView(ListView):
    model = Category
    template_name = 'admin_p/AdminCategories.html'


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'category__title': ['exact'],
        }


@method_decorator(login_required, name='dispatch')
class PanelProductView(ListView):
    """
    все продукты с фильтром по категориям и пагинацией
    """
    model = Product
    template_name = 'admin_p/AdminProducts.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category').values('id', 'title', 'category__title').order_by(
            'category__title')

        # Добавление фильтрации по категории из параметров запроса (если указана)
        category_title = self.request.GET.get('category_title')
        if category_title:
            queryset = queryset.filter(category__title=category_title)
        self.categories = list(set(item['category__title'] for item in queryset))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        return context


@method_decorator(login_required, name='dispatch')
class PanelCategoryDetailView(View):

    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        if category:
            form = CategoryForm(instance=category)
            products = Product.objects.filter(category=pk).only('id', 'title', 'price')
            return render(request, 'admin_p/AdminCategoryDetail.html',
                          {'form': form, 'category': category, 'products': products})
        else:
            return redirect('panel_category')

    def post(self, request, pk):
        form = CategoryForm(request.POST)
        category = Category.objects.get(id=pk)
        if form.is_valid():
            category.title = form.cleaned_data['title']
            category.save()
            return redirect(to='/panel/category/')
        else:
            return render(request, 'admin_p/AdminCategoryDetail.html', {'form': form, 'category': category})


@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin_p/AdminCreateCategory.html'
    success_url = reverse_lazy('panel_category')


@method_decorator(login_required, name='dispatch')
class PanelProductDetailView(View):

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        form = ProductForm(instance=product)
        return render(request, 'admin_p/AdminProductDetail.html', {'product': product, 'form': form})

    def post(self, request, pk):
        form = ProductForm(request.POST, request.FILES)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            product.title = form.cleaned_data['title']
            product.price = form.cleaned_data['price']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.photo = form.cleaned_data['photo']
            print(form.cleaned_data)
            print(form.cleaned_data['photo'])
            print('*'*60)
            product.save()
            return redirect(to='/panel/products/')
        else:

            return render(request, 'admin_p/AdminProductDetail.html', {'product': product, 'form': form})


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_p/AdminCreateProduct.html'
    success_url = reverse_lazy('panel_product')


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(View):
    def get(self, request, pk):
        Product.objects.get(id=pk).delete()
        return redirect(to='/panel/products/')


@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(View):

    def get(self, request, pk):
        Category.objects.get(id=pk).delete()
        return redirect(to='/panel/category/')
