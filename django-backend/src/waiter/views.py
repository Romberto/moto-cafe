from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from tables.models import TableModel
from orders.models import Orders, ItemOrders
from waiter.forms import WaiterForm
from waiter.permissions.permissions import IsAuthenticatedAndAdminOrReadOnly
from waiter.serializers import WaiterSerializer, WaiterCreateSerializer


def user_is_waiter(user):
    return user.groups.filter(name='Waiter').exists()


class WaiterViewSet(ModelViewSet):
    queryset = User.objects.filter(groups__name='Waiter')
    serializer_class = WaiterSerializer
    permission_classes = [IsAuthenticatedAndAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return WaiterSerializer
        return WaiterCreateSerializer

    def create(self, request, *args, **kwargs):
        # Создаем пользователя
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Добавляем пользователя в группу "Waiter"
        user = serializer.instance
        waiter_group, created = Group.objects.get_or_create(name='Waiter')
        if created:
            # Получите типы контента для моделей Order и ItemOrder
            order_content_type = ContentType.objects.get_for_model(Orders)
            item_order_content_type = ContentType.objects.get_for_model(ItemOrders)

            # Создайте и получите необходимые разрешения
            can_add_order_permission, created = Permission.objects.get_or_create(
                codename='can_add_order',
                name='Can add Order',
                content_type=order_content_type
            )

            can_change_order_permission, created = Permission.objects.get_or_create(
                codename='can_change_order',
                name='Can change Order',
                content_type=order_content_type
            )

            can_add_item_order_permission, created = Permission.objects.get_or_create(
                codename='can_add_item_order',
                name='Can add ItemOrder',
                content_type=item_order_content_type
            )

            can_change_item_order_permission, created = Permission.objects.get_or_create(
                codename='can_change_item_order',
                name='Can change ItemOrder',
                content_type=item_order_content_type
            )

            # Присвойте разрешения группе "Waiter"
            waiter_group.permissions.add(can_add_order_permission)
            waiter_group.permissions.add(can_change_order_permission)
            waiter_group.permissions.add(can_add_item_order_permission)
            waiter_group.permissions.add(can_change_item_order_permission)
        user.groups.add(waiter_group)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        group_name = 'Waiter'  # Замените на имя группы, которую вы хотите удалить
        try:
            group = Group.objects.get(name=group_name)
            users_to_delete = User.objects.filter(groups=group)
            users_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class WaitersView(ListView):
    model = User
    template_name = 'waiter/Waiters.html'
    context_object_name = 'waiters'

    def get_queryset(self):
        target_groups = ['Waiter']
        queryset = User.objects.filter(groups__name__in=target_groups)
        return queryset


class EditWaiterView(View):
    def get(self, request, pk):
        try:
            waiter = User.objects.get(id=pk)
            form = WaiterForm(instance=waiter)
            data = {
                'form': form,
                'waiter': waiter
            }
            return render(request, 'waiter/WaiterEdit.html', data)
        except ObjectDoesNotExist:
            return render(request, 'waiter/WaiterEdit.html')

    def post(self, request, pk):
        form = WaiterForm(request.POST)
        waiter = User.objects.get(id=pk)
        if form.is_valid():
            waiter.first_name = form.cleaned_data['first_name']
            waiter.last_name = form.cleaned_data['last_name']
            waiter.save()
            return redirect(reverse_lazy('all_waiters'))
        else:
            data = {
                'form': form,
                'waiter': waiter
            }
            return render(request, 'waiter/WaiterEdit.html', data)


class DeleteWaiterView(DeleteView):
    model = User
    template_name = 'waiter/WaiterDelete.html'
    success_url = reverse_lazy('panel')

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            return self.render_to_response({'error': str(e)})


class CreateWaiter(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'waiter/WaiterCreate.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Waiter')
            user.groups.add(group)
            return redirect(reverse_lazy('all_waiters'))
        else:
            variables = {
                'form': form
            }
            return render(request, 'waiter/WaiterCreate.html', variables)