import json

from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import DetailView, DeleteView

from orders.models import ItemOrders, Orders
from product.models import Product
from waiter.views import login_admin
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
            'order_id': item.order_id.id,
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
        is_admins = request.user.groups.filter(name="Admins").exists()
        if table.owner_officiant == request.user and not is_admins:  # является ли user официантом этого стола
            orders = get_orders_id(pk)

            return render(request, 'tables/TableDetail.html', {'data': data, 'orders': orders})
        elif is_admins:  # является ли user администратором
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


@method_decorator(login_required, name='dispatch')
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
@require_POST
@login_required
def create_table(request):
    """
    ajax запрос на открытие стола
    """
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


@require_POST
@login_required
def add_order(request):
    """
    ajax запрос на добавление заказов в стол
    """
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        data_list = request.POST.get('data_list')
        order = Orders.objects.get(table_id__name=table_name)
        data_python_list = json.loads(data_list)
        objects_list = []
        for item in data_python_list:
            product = Product.objects.get(id=item['product_id'])
            order_element = ItemOrders.objects.filter(product_id=product, order_id=order).select_related('product_id',
                                                                                                         'order_id')
            if not order_element:
                objects_list.append(
                    ItemOrders(order_id=order, product_id=product, count=item['count'])
                )
            else:
                order_element[0].count += item['count']
                order_element[0].save()
        ItemOrders.objects.bulk_create(
            objects_list
        )
        data = {
            'success': True
        }
        return JsonResponse(data)


@require_GET
@login_admin
def close_empty_check(request):
    """
    ajax запрос на закрытие пустого стола
    """
    number_table = request.GET.get('table')
    try:
        table = TableModel.objects.get(name=int(number_table))
        table.owner_officiant = None
        table.save()
        order = Orders.objects.get(table_id=table)
        order.delete()
        data = {
            'success': True
        }
    except TableModel.DoesNotExist:
        data = {
            'success': False
        }
    return JsonResponse(data)


@require_POST
@login_admin
def close_full_check(request):
    """
    ajax запрос для закрытия стола с заказом
    """
    table_name = request.POST.get('table')
    order = Orders.objects.get(table_id__name=table_name, status='open')
    order.table_id.owner_officiant = None
    order.table_id.save()
    order.status = 'pay'
    order.delete()



    data = {
        'success': False
    }
    return JsonResponse(data)


@require_GET
@login_admin
def api_edit_product_quality(request):
    order_id = request.GET.get('order')
    count = request.GET.get('count')
    order = ItemOrders.objects.get(id=int(order_id))
    if int(count) != order.count:
        if int(count) == 0:
            order.delete()
        else:
            order.count = count
            order.save()
        data = {
            'success': True
        }
    else:
        data = {
            'success': False
        }
    return JsonResponse(data)