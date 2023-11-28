from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from category.models import Category
from user_auth.forms import AuthForm


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm
    template_name = 'user_auth/registration.html'


class MyLogoutView(LogoutView):
    template_name = 'category/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Category.objects.all()
        return context


class ResetPassword(View):
    def get(self, request, pk):
        if not request.user.groups.filter(name='Admins').exists():
            return HttpResponse("У вас нет прав для сброса пароля.", status=403)
        else:
            user = User.objects.get(id=pk)
            return render(request, 'user_auth/resetpassword.html', {'waiter': user})

    def post(self, request, pk):
        password = request.POST.get('password')
        user = User.objects.get(id=pk)
        user.set_password(password)
        user.save()
        return redirect(reverse_lazy('panel'))
