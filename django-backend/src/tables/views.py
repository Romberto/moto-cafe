from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, DeleteView

from orders.models import ItemOrders, Orders
from product.models import Product
from .models import TableModel


def get_orders_id(pk: int):
    query = ItemOrders.objects.select_related('order_id', 'product_id', 'order_id__table_id').filter(
        order_id__table_id=pk).annotate(total_price=F('product_id__price') * F('count'))
    result = {
        'itemOrders': [],
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
    return result


@method_decorator(login_required, name='dispatch')
class PanelTable(View):
    def get(self, request, pk: int):
        table = TableModel.objects.get(id=pk)
        data = {
            'is_admin': False,
            'table': table
        }
        if table.owner_officiant == request.user:  # является ли user официантом этого стола
            orders = get_orders_id(pk)

            return render(request, 'tables/TableDetail.html', {'data': data, 'orders': orders})
        elif request.user.groups.filter(name="Admins").exists():  # является ли user администратором
            data['is_admin'] = True
            orders = get_orders_id(pk)
            return render(request, 'tables/TableDetail.html', {'data': data, 'orders': orders})
        else:
            if not table.owner_officiant:
                return render(request, 'tables/TableDetail.html', {'data': data})
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


@method_decorator(login_required, name='dispatch')
def build_menu_product():
    menu_list = form_menu_products()
    html = ''
    html += "<ul class='ps-0 d-flex flex-column'>"
    for item_menu in menu_list:
        html += "<li>"
        html += f"<button href='#' class='btn btn-info'>{item_menu}</button>"

        html += '</li>'
    html += "</ul>"


# открытие счёта
def create_table(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        try:
            table = TableModel.objects.get(name=number)
            table.owner_officiant = request.user
            table.save()
            order = Orders.objects.create(table_id=table)
            data = {

                'table': 'ok',
            }
        except TableModel.DoesNotExist:
            data = {

                'error': 'not model',
            }

        return JsonResponse(data)
    else:
        # Обработка случаев, когда запрос не AJAX или не POST
        pass