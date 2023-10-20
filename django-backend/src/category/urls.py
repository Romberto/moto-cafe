from django.urls import path

from category.views import CategoryView, CategoryItemView

urlpatterns = [
    path('', CategoryView.as_view(), name='category'),
    path('<int:pk>', CategoryItemView.as_view(), name="category_item"),

]