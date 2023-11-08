from django.urls import path

from admin_p.views import PanelView, PanelCategoryView, PanelProductView, PanelCategoryDetailView, \
    PanelProductDetailView, ProductCreateView, ProductDeleteView, CategoryCreateView, CategoryDeleteView, PanelTable, \
    PanelTableDelete

urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
    path('category/', PanelCategoryView.as_view(), name='panel_category'),
    path('products/', PanelProductView.as_view(), name='panel_product'),
    path('products/create', ProductCreateView.as_view(), name="panel_product_create"),
    path('category/<int:pk>', PanelCategoryDetailView.as_view(), name='panel_category_detail'),
    path('category/create', CategoryCreateView.as_view(), name='panel_category_create'),
    path('product/<int:pk>', PanelProductDetailView.as_view(), name='product_panel_detail'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name="product_delete"),
    path('category/dalete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),
    path('table/<int:pk>', PanelTable.as_view(), name="panel_table_detail"),
    path('table/delete/<int:pk>', PanelTableDelete.as_view() ,name='delete_table')
]
