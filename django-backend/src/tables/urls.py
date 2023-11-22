from django.urls import path

from tables.models import TableModel
from tables.views import PanelTable, PanelTableDelete, build_menu_product, create_table, add_order

urlpatterns = [
    path('table/<int:pk>', PanelTable.as_view(), name="panel_table_detail"),
    path('table/delete/<int:pk>', PanelTableDelete.as_view(), name='delete_table'),
    path('ajax/get_menu', build_menu_product),
    path('create_table/', create_table, name='create_table'),
    path('add_order/', add_order, name='add_order')

]
