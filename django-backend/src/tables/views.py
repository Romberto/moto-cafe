from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, DeleteView

from orders.models import ItemOrders
from product.models import Product
from .models import TableModel


@method_decorator(login_required, name='dispatch')
class PanelTable(View):
    def get(self, request, pk: int):
        query = ItemOrders.objects.select_related('order_id', 'product_id', 'order_id__table_id').filter(
            order_id__table_id=pk).annotate(total_price=F('product_id__price') * F('count'))
        result = {
            'itemOrders': [],
            'table': {'name': None, 'owner_officiant': None},
            'is_admin': False,
            'is_onwer': False,
            'full_price': 0

        }
        for item in query:
            result['itemOrders'].append({
                'id': item.id,
                'product_title': item.product_id.title,
                'product_price': int(item.product_id.price),
                'count': item.count,
                'total_price': int(item.total_price)
            })
            result['full_price'] += item.total_price
            if result['table']['name'] is None and result['table']['owner_officiant'] is None:
                result['table']['name'] = item.order_id.table_id.name
                result['table']['owner_officiant'] = item.order_id.table_id.owner_officiant.id

        if result['table']['owner_officiant'] == request.user.id or result['table']['owner_officiant'] == None:
            result['is_onwer'] = True
            if result['table']['owner_officiant'] == None:
                result['is_onwer'] = False
                result['table']['name'] = pk
            return render(request, 'tables/TableDetail.html', {'result': result})
        elif request.user.groups.filter(name="Admins").exists():
            result['is_admin'] = True
            return render(request, 'tables/TableDetail.html', {'result': result})
        else:
            return redirect(reverse('panel'))


@method_decorator(login_required, name='dispatch')
class PanelTableDelete(DeleteView):
    model = TableModel
    template_name = 'tables/TableDelete.html'


def form_menu_products():
    products = Product.objects.all().select_related('category').only('id', 'title', 'price', 'category__title')
    result = {}
    for product in products:
        if not product.category.title in result:
            result.update({product.category.title: [product]})
        else:
            result[product.category.title].append(product)
    return result


def build_menu_product():
    menu_list = form_menu_products()
    html = ''
    html += "<ul class='ps-0 d-flex flex-column'>"
    for item_menu in menu_list:
        html += "<li>"
        html += f"<button href='#' class='btn btn-info'>{item_menu}</button>"

        html += '</li>'
    html += "</ul>"